import json

import pytest

from app import app
from app.model.user import User


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


def test_create_event(setup_app):
    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    setup_app["client_test"].get('/user/login', headers={"Content-Type": "application/json"},
                                 data=payload)

    titre_event = "Enenement de Test"
    date_event = "11/08/2020 12:30"
    description = "Test de creation event"

    payload = json.dumps({
        "titre": titre_event,
        "date": date_event,
        "description": description
    })

    response = setup_app["client_test"].post('/user/evenement', headers={"Content-Type": "application/json"},
                                             data=payload)

    assert str == type(response.json['message'])
    assert "Evenement is created" == response.json['message']
    assert 200 == response.status_code


def test_create_evenement(setup_app):
    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    setup_app["client_test"].get('/user/login', headers={"Content-Type": "application/json"},
                                 data=payload)

    titre_event = "Enenement de Test"
    date_event = "11/08/2020 12:30"
    description = "Test de creation event"

    payload = json.dumps({
        "titre": titre_event,
        "description": description,
        "date": date_event
    })

    setup_app["client_test"].post('/user/evenement', headers={"Content-Type": "application/json"},
                                  data=payload)


def test_get_event(setup_app):
    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    titre_event = "Enenement de Test"
    date_event = '2020-11-08 12:30:00'
    description = "Test de creation event"

    setup_app["client_test"].get('/user/login', headers={"Content-Type": "application/json"},
                                 data=payload)

    response = setup_app["client_test"].get('/user/evenement')

    assert dict == type(response.json['evenements'])

    event = response.json['evenements']["0"]

    assert titre_event == event["titre"]
    assert description == event["description"]
    assert date_event == event["date"]
    assert username == event["autheur"]

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

    user = User.query.filter_by(username=username).first()
    id_event = 0
    for event in user.evenements_cree:
        id_event = event.id

    payload = json.dumps({
        "id_event": id_event
    })

    response = setup_app["client_test"].delete('/user', headers={"Content-Type": "application/json"},
                                               data=payload)
    assert 200 == response.status_code
