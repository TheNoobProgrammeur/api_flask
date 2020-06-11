import json

import pytest

from app import app


@pytest.fixture
def setup_app():
    return {
        "client_test": app.test_client()
    }


def test_register(setup_app):
    username = "antoine_test"
    password = "azerty"
    email = "test@test.gouv"

    payload = json.dumps({
        "username": username,
        "email": email,
        "password": password
    })

    response = setup_app["client_test"].post('/user/register', headers={"Content-Type": "application/json"},
                                             data=payload)

    assert str == type(response.json['message'])
    assert "Your is resisted" == response.json['message']
    assert 200 == response.status_code


def test_login(setup_app):
    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    response = setup_app["client_test"].get('/user/login', headers={"Content-Type": "application/json"},
                                            data=payload)

    assert str == type(response.json['message'])
    assert "Your is identified" == response.json['message']
    assert 200 == response.status_code


def test_delete(setup_app):
    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    setup_app["client_test"].get('/user/login', headers={"Content-Type": "application/json"},
                                            data=payload)

    response = setup_app["client_test"].delete('/user/')
    assert 200 == response.status_code
