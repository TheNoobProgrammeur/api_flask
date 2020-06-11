import datetime
import logging
from functools import wraps

import jwt
from flask import session, Response

from app import app


def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if "api_sessions_token" not in session:
            return {"response": "ERROR : token incorrect"}, 403

        token = session['api_sessions_token']
        if not decode_auth_token(token):
            del session['api_sessions_token']
            return {"response": "ERROR : token expiret"}, 403

        return func(*args, **kwargs)

    return check_token


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
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
    except Exception as e:
        return e


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


def get_id_by_token(auth_token):
    return decode_auth_token(auth_token)
