# Daniel Holmes
# __init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['ELEPHANT_POSTGRESQL_DB']

heroku = Heroku(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes
