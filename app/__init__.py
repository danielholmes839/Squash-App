# Daniel Holmes
# __init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_heroku import Heroku


class DevelopmentConfig(object):
    def __init__(self):
        self.DEBUG = True
        self.SQLAlCHEMY_DATABASE_URI = 'sqlite://test.db'
        self.SECRET_KEY = 'secret'


class ProductionConfig(object):
    def __init__(self):
        self.DEBUG = False
        self.SQLAlCHEMY_DATABASE_URI = os.environ['DB_URI']
        self.SECRET_KEY = os.environ['SECRET_KEY']


app = Flask(__name__)
app.config.from_object(ProductionConfig())

heroku = Heroku(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes
