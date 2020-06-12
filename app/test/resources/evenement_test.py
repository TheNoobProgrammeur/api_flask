import json

import pytest

from app import app


@pytest.fixture
def setup_app():
    username = "antoine_test"
    password = "azerty"
    email = "test@test.ts"

    payload_user1 = json.dumps({
        "username": username,
        "email": email,
        "password": password
    })

    username2 = "antoine_test2"
    password2 = "azerty2"
    email2 = "test2@test.ts"

    payload_user2 = json.dumps({
        "username": username2,
        "email": email2,
        "password": password2
    })

    return {
        "user1": payload_user1,
        "user2": payload_user2,
        "client_test": app.test_client()
    }


@pytest.fixture
def gestion_user(setup_app):
    aplication = setup_app["client_test"]
    payload_user1 = setup_app["user1"]
    payload_user2 = setup_app["user2"]

    aplication.post('/user/register', headers={"Content-Type": "application/json"},
                    data=payload_user1)

    aplication.post('/user/register', headers={"Content-Type": "application/json"},
                    data=payload_user2)
    yield

    aplication.get('/user/login', headers={"Content-Type": "application/json"},
                   data=payload_user1)

    aplication.delete('/user/')

    aplication.get('/user/login', headers={"Content-Type": "application/json"},
                   data=payload_user2)

    aplication.delete('/user/')


def test_get_evenement(setup_app):
    aplication = setup_app["client_test"]

    response = aplication.get('/evenement',  headers={"Content-Type": "application/json"})

    assert str == type(response.json['message'])
    assert dict == type(response.json['evenements'])
    assert 200 == response.status_code
