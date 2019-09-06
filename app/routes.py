# Daniel Holmes
# routes.py

import atexit

from flask import render_template, url_for, redirect, request
from sqlalchemy import desc
from apscheduler.schedulers.background import BackgroundScheduler

from app import app, db, rankenstein, auth, maintenance
from app.models import Player, Result
from app.forms import PredictionForm
from app.predictions import get_prediction


@app.before_first_request
def schedule_tasks():
    """ Schedule database updates """
    scheduler = BackgroundScheduler()
    scheduler.add_job(rankenstein.update, 'interval', hours=12)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())


@app.route('/')
@app.route('/home')
def home():
    """ Home page """
    return render_template('home.html', title='Home')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """ Prediction Form """
    form = PredictionForm()
    players = Player.query.order_by(Player.name).all()

    if form.validate_on_submit():

        # Redirect to a prediction between two players
        p1 = Player.query.filter_by(name=form.player1.data).first()
        p2 = Player.query.filter_by(name=form.player2.data).first()
        return redirect(url_for('prediction', p1=p1.id, p2=p2.id))

    return render_template('predict.html', form=form, players=players, title='New Prediction')


@app.route('/prediction')
def prediction():
    """ Prediction Display """
    p1 = Player.query.get(request.args.get('p1'))
    p2 = Player.query.get(request.args.get('p2'))
    _, _, _, message = get_prediction(p1, p2)

    return render_template('prediction.html', prediction=message, player1=p1, player2=p2, title='Prediction')


@app.route('/results')
def results():
    """ Results """
    r = Result.query.order_by(desc(Result.date)).limit(50).all()
    return render_template('results.html', results=r, title='Results')


@app.route('/rankings')
def rankings():
    """ Rankings """
    players = Player.query.order_by(-Player.rating).all()
    return render_template('rankings.html', players=players, title='Rankings')


@app.route('/api/create-key', methods=['POST'])
def create_key():
    """ Create an API key """
    credentials = request.get_json(force=True)
    return auth.create(credentials)


@app.route('/api/create-database', methods=['POST'])
@auth.required()
def create_database():
    """ Reset the data base """
    return maintenance.create_database()


@app.route('/api/reset-database', methods=['POST'])
@auth.required()
def reset_database():
    """ Reset the data base """
    return maintenance.reset_db()


@app.route('/api/update-players', methods=['POST'])
@auth.required()
def update_players():
    """ Update players """
    return rankenstein.update_rankings()


@app.route('/api/update-results', methods=['POST'])
@auth.required()
def update_results():
    """ Update results """
    return rankenstein.update_results()


@app.route('/api/update', methods=['POST'])
@auth.required()
def update():
    """ Update players and results """
    return rankenstein.update()
