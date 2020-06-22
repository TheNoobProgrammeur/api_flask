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

    res = setup_app["client_test"].post('/user/register', headers={"Content-Type": "application/json"},
                                        data=payload)

    token = res.json['token']

    yield

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
