# Daniel Holmes
# predictions.py

import joblib
from app import rankenstein

model = joblib.load('app/model.joblib')


def get_vector(p1, p2):
    """ Get the vector used to make the prediction """

    # Head to head record are not stored and must be obtained from rankenstein
    p1_hh = rankenstein.get_hh(p1, p2)
    p2_hh = 100 - p1_hh
    d_hh = p2_hh - p1_hh

    # Stored Stats
    d_rating = p2.rating - p1.rating
    d_trend = p2.trend - p1.trend
    d_streak = p2.streak - p1.streak

    try:    # Possibility of division by 0 when calculating season win rate
        p1_season_wr = p2.wins / p2.matches
    except ZeroDivisionError:
        p1_season_wr = 50

    try:
        p2_season_wr = p2.wins / p2.matches
    except ZeroDivisionError:
        p2_season_wr = 50

    d_season_win_percentage = p2_season_wr - p1_season_wr
    d_rust = (p2.last_played - p1.last_played).days

    return [d_rating, d_hh, d_trend, d_streak, d_season_win_percentage, d_rust]


def get_player_scores(prediction):
    """ Get each players score """
    if prediction < 0:
        p1_score = 3
        p2_score = 3 - abs(int(prediction))

    else:
        p1_score = 3 - abs(int(prediction))
        p2_score = 3

    return p1_score, p2_score


def get_score_string(prediction):
    """
    convert score labels 1, 2, 3, -1, -2, 3
    to scores 3-0, 3-1, 3-2
    """

    return f'3-{3 - abs(prediction)}'


def get_winner_loser(p1, p2, prediction):
    """ Get the winner and loser """
    if prediction < 0:
        winner = p1.name
        loser = p2.name

    else:
        winner = p2.name
        loser = p1.name

    return winner, loser


def get_prediction_message(prediction, p1, p2):
    """ Gets the message for the prediction """
    winner, loser = get_winner_loser(p1, p2, prediction)
    score = get_score_string(prediction)

    return f'{winner} will win against {loser} {score}'


def get_prediction(p1, p2):
    """ get prediction """
    vector = get_vector(p1, p2)
    prediction = model.predict([vector])[0]

    p1_score, p2_score = get_player_scores(prediction)

    return prediction, p1_score, p2_score, get_prediction_message(prediction, p1, p2)

