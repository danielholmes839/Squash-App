# Daniel Holmes
# forms.py

from flask import flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from app.models import Player


class PredictionForm(FlaskForm):
    """ Prediction Form """
    name = 'Prediction'
    player1 = StringField('Player 1')
    player2 = StringField('Player 2')
    submit = SubmitField('Predict')

    def validate(self):
        """ Validate the form """
        valid = True
        if not super().validate():
            valid = False

        names = [player.name for player in Player.query.order_by(Player.name).all()]

        self.player1.data = self.player1.data.strip()
        self.player2.data = self.player2.data.strip()

        if self.player1.data == self.player2.data:
            flash('Players cannot be the same')
            valid = False

        if not self.player1.data in names:
            flash(f'Could not find: {self.player1.data}')
            valid = False

        if not self.player2.data in names:
            flash(f'Could not find: {self.player2.data}')
            valid = False

        return valid