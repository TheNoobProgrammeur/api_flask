import json

import pytest

from app import app


@pytest.fixture
def setup_app():
    return {
        "client_test": app.test_client()
    }


@pytest.fixture
def gestion_user(setup_app):
    username = "antoine_test"
    password = "azerty"
    email = "test@test.gouv"

    payload = json.dumps({
        "username": username,
        "email": email,
        "password": password
    })

    setup_app["client_test"].post('/user/register', headers={"Content-Type": "application/json"},
                                        data=payload)



    yield

    res = setup_app["client_test"].post('/user/login', headers={"Content-Type": "application/json"},
                                        data=payload)
    token = res.json['token']
    setup_app["client_test"].delete('/user',
                                    headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})


def test_smoke(setup_app, gestion_user):
    response = setup_app["client_test"].get('ping/smoke')

    assert str == type(response.json['response'])
    assert 200 == response.status_code


def test_ping(setup_app, gestion_user):
    response = setup_app["client_test"].get('ping/smoke')

    assert str == type(response.json['response'])
    assert 200 == response.status_code


def test_token_error(setup_app, gestion_user):
    response = setup_app["client_test"].get('ping', headers={"Content-Type": "application/json",
                                                             "Authorization": "Bearer azerty"})

    assert str == type(response.json['response'])
    assert 403 == response.status_code


def test_session(setup_app, gestion_user):
    response = setup_app["client_test"].get('ping')

    assert str == type(response.json['response'])
    assert 200 == response.status_code


def test_session_expired_error(setup_app, gestion_user):
    setup_app["client_test"].get('/user/logout')

    response = setup_app["client_test"].get('ping')

    assert str == type(response.json['response'])
    assert 403 == response.status_code
