import hashlib
import json

import pytest

from app import app, db
from app.model.user import User


@pytest.fixture
def setup_app():
    userInfo = {
        "username": "antoine_test",
        "password": "azerty",
        "email": "test@test.gouv"
    }

    return {
        "userInfo": userInfo,
        "client_test": app.test_client()
    }


@pytest.fixture
def gestion_user(setup_app):
    userInfo = setup_app["userInfo"]

    db.session()

    user = User()
    user.username = userInfo["username"]
    user.email = userInfo["email"]
    user.password_hash = hashlib.sha256(userInfo["password"].encode("UTF-8")).hexdigest()

    db.session.add(user)
    db.session.commit()

    yield
    db.session()
    db.session.delete(user)
    db.session.commit()


@pytest.fixture
def login_user(setup_app):
    userInfo = setup_app["userInfo"]
    application = setup_app["client_test"]

    payload_user = json.dumps({
        "username": userInfo["username"],
        "email": userInfo["password"],
    })

    application.get('/user/login', data=payload_user)

    return {
        "client_test": application
    }

def test_smoke(setup_app, gestion_user):
    application = setup_app["client_test"]

    response = application.get('ping/smoke')

    assert str == type(response.json['response'])
    assert 200 == response.status_code


def test_ping(setup_app, gestion_user):
    application = setup_app["client_test"]
    response = application.get('ping/smoke')

    assert str == type(response.json['response'])
    assert 200 == response.status_code


def test_token_error(setup_app, gestion_user):
    application = setup_app["client_test"]

    response = application.get('ping', headers={"Content-Type": "application/json",
                                                             "Authorization": "Bearer azerty"})

    assert str == type(response.json['response'])
    assert 403 == response.status_code


def test_session(setup_app, gestion_user, login_user):

    application = login_user["client_test"]
    response = application.get('ping')

    assert str == type(response.json['response'])
    assert 200 == response.status_code


def test_session_expired_error(setup_app, gestion_user, login_user):
    application = login_user["client_test"]
    application.get('/user/logout')

    response = setup_app["client_test"].get('ping')

    assert str == type(response.json['response'])
    assert 403 == response.status_code
