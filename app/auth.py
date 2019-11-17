# Daniel Holmes
# auth.py

import os
from flask import request
from functools import wraps

from app import bcrypt, db
from app.models import APIKey


def required():
    """
    API Key required authorization decorator
    request should contain a 'username' and 'password' key
    """
    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if authenticate():
                # continue to route
                return f(*args, **kwargs)
            else:
                # failed to authenticate
                return 'Authentication Failed'
        return wrapper
    return inner_function


def master():
    """
    Master Key required authorization decorator
    Used to create/reset the database and create new API Keys
    request should container 'master' key that matches os.environ['MASTER-KEY']
    """
    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            credentials = request.get_json(force=True)
            if credentials['master'] == os.environ['MASTER_KEY']:
                # continue to route
                return f(*args, **kwargs)
            else:
                return 'Authentication Failed'
        return wrapper
    return inner_function


def create(credentials):
    """
    Create new API keys
    Called from route that requires master auth
    """
    existing_key = APIKey.query.filter_by(username=credentials['username']).first()

    if not existing_key:
        key = APIKey(
            username=credentials['username'],
            password=bcrypt.generate_password_hash(credentials['password']).decode('utf-8')
        )
        db.session.add(key)
        db.session.commit()
        return 'Successfully Created Key'

    else:
        return 'Username Already Taken'


def authenticate():
    """ Authenticate the API request """
    try:
        credentials = request.get_json(force=True)
        key = APIKey.query.filter_by(username=credentials['username']).first()

        if bcrypt.check_password_hash(key.password, credentials['password']):
            return True

    except Exception:
        pass

    return False

