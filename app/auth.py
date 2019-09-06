# Daniel Holmes
# auth.py

import os
from flask import request
from functools import wraps

from app import bcrypt, db
from app.models import APIKey


def create(credentials):
    """ Create new API keys """
    if credentials['key'] == os.environ['MASTER_KEY']:

        existing_key = APIKey.query.filter_by(username=credentials['username']).first()

        if not existing_key:

            key = APIKey(
                username=credentials['username'],
                password=bcrypt.generate_password_hash(credentials['password']).decode('utf-8')
            )

            db.session.add(key)
            db.session.commit()

            return 'Successfully Created Key'

        return 'Failed to create a new API key - that username is already taken'

    return 'Authentication Failed'


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


def required():
    """ Basic Authorization Required """
    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            authenticated = authenticate()

            if authenticated:
                # Original function
                return f(*args, **kwargs)

            return 'Authentication Failed'

        return wrapper

    return inner_function
