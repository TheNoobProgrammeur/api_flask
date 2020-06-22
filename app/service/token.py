import datetime
import logging
from functools import wraps

import jwt
from flask import session, Response

from app import app
from app.model.user import User


def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        """
        Decorateur qui verifie la validiter du token de session
        :param args:
        :param kwargs:
        :return:
        """
        if "api_sessions_token" not in session:
            return {"response": "ERROR : token incorrect"}, 403, {'Access-Control-Allow-Origin': '*'}

        token = session['api_sessions_token']
        if not decode_auth_token(token):
            del session['api_sessions_token']
            return {"response": "ERROR : token expiret"}, 403, {'Access-Control-Allow-Origin': '*'}

        return func(*args, **kwargs)

    return check_token


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }

    return jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        logging.error('Signature expired. Please log in again.')
        return False
    except jwt.InvalidTokenError:
        logging.error('Invalid token. Please log in again.')
        return False


def get_user_by_token():
    """
    Permet de renvoyé le user courent grasse au token de session
    :return User
    """

    if 'api_sessions_token' not in session:
        return None
    token = session['api_sessions_token']
    id = decode_auth_token(token)
    user = User.query.filter_by(id=id).first()
    return user
