# Daniel Holmes
# models.py

import datetime as dt
from app import db


class Player(db.Model):
    """ Player model """

    # Player Background
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    club = db.Column(db.String, nullable=False)

    # Player Stats
    matches = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    streak = db.Column(db.Integer, nullable=False)
    trend = db.Column(db.Integer, nullable=False)
    last_played = db.Column(db.DATE, nullable=False)


class Result(db.Model):
    """ Result model """
    id = db.Column(db.Integer, unique=True, primary_key=True)
    p1_id = db.Column(db.Integer)
    p2_id = db.Column(db.Integer)

    p1 = db.Column(db.String, nullable=False)
    p2 = db.Column(db.String, nullable=False)

    p1_score = db.Column(db.Integer, nullable=False)
    p2_score = db.Column(db.Integer, nullable=False)

    pred_p1_score = db.Column(db.Integer, nullable=False)
    pred_p2_score = db.Column(db.Integer, nullable=False)

    upset = db.Column(db.Boolean, nullable=False)

    date = db.Column(db.Date, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)


class APIKey(db.Model):
    """ API key model """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.datetime.utcnow())
