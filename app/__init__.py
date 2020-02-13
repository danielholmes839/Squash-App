# Daniel Holmes
# __init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_heroku import Heroku


def development_setup(app):
    """ app config for development """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['DEBUG'] = True
    os.environ['MASTER_KEY'] = 'master_key'
    os.environ['MODE'] = 'development'


def production_setup(app):
    """ app config for heroku """
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['DEBUG'] = False


app = Flask(__name__)

if 'MODE' in os.environ and os.environ['MODE'] == 'production':
    production_setup(app)
else:
    development_setup(app)

print(f'Running app in {os.environ["MODE"]} mode')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
heroku = Heroku(app)

from app import routes
