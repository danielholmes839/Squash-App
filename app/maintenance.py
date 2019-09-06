# Daniel Holmes
# maintenance.py

from app import db


def create_database():
    """ Creates the database """
    db.create_all()
    db.session.commit()
    return 'Successfully Created Database'


def reset_db():
    """ Resets the database """
    db.drop_all()
    db.create_all()
    db.session.commit()
    return 'Successfully Reset Database'