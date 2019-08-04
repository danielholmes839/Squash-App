# Daniel Holmes
# 2019-07-13
# rankenstein.py
# functions for using rankenstein APIs

import requests
import datetime as dt
from bs4 import BeautifulSoup
from app.models import Player, Result
from app import db
from app.predictions import get_prediction


def get_hh(p1, p2):
    """ Get a players head to head win rate in a match up """
    result = requests.get(f'https://odsa.rankenstein.ca/profile.pl?action=head&id={p1.id}').json()
    head_to_head = result['aaData']

    for match_up in head_to_head:
        opponent_name = BeautifulSoup(match_up[0], 'html.parser').a.string

        if opponent_name == p2.name:
            p1_win_rate = int(match_up[4].strip(' %'))
            return p1_win_rate

    return 50   # New match up assume even win rate


def get_rankings():
    """ Gets rankings from rankenstein """
    result = requests.get('https://odsa.rankenstein.ca/api.pl?action=rankings').json()
    return result['rankings'], result['lastUpdate']


def get_results():
    """ Get results from rankenstein """
    return requests.get('https://odsa.rankenstein.ca/api.pl?action=results').json()[:100]


def create_player(json):
    """ Creates a player database record from a player ranking """
    return Player(
        id=json['player']['id'],
        name=json['player']['name'],
        club=json['club'],
        matches=json['matches'],
        wins=json['wins'],
        losses=json['losses'],
        rating=json['rating'],
        streak=json['streak'],
        trend=json['trend'],
        last_played=dt.datetime.strptime(json['lastMatch'], '%Y-%m-%d')
    )


def create_result(json):
    """ Create a result with a prediction from results from rankenstein """
    p1 = Player.query.get(int(json['winnerId']))
    p2 = Player.query.get(int(json['loserId']))
    year, month, day = json['date'].split('-')

    if p1 and p2:
        _, pred_p1_score, pred_p2_score, _ = get_prediction(p1, p2)
        upset = p1.rating < p2.rating

        return Result(
            id=json['id'],
            p1_id=json['winnerId'],
            p2_id=json['loserId'],
            p1=json['winnerName'],
            p2=json['loserName'],
            p1_score=3,
            p2_score=json['resultDetails']['loserScore'],
            pred_p1_score=pred_p1_score,
            pred_p2_score=pred_p2_score,
            upset=upset,
            date=dt.date(year=int(year), month=int(month), day=int(day)),
            entry_date=dt.datetime.strptime(json['entryDate'], '%Y-%m-%d %H:%M:%S')
        )

    return None


def update_rankings():
    """ Update all players in the data base """
    db.session.query(Player).delete()
    player_rankings, _ = get_rankings()

    for ranking in player_rankings:
        player = create_player(ranking)
        db.session.add(player)

    db.session.commit()


def update_results():
    """ Update results """
    results = get_results()

    for json in results:

        if not Result.query.get(int(json['id'])):

            result = create_result(json)

            if result:
                db.session.add(result)

    db.session.commit()


def update():
    """ Update players and results """
    update_rankings()
    update_results()