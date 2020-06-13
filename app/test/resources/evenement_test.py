import json

import pytest

from app import app, db
from app.model.evenement import Evenement


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

    titre_event = "Enenement de Test"
    date_event = "11/08/2020 12:30"
    description = "Test de creation event"

    payload_event = json.dumps({
        "titre": titre_event,
        "description": description,
        "date": date_event
    })

    return {
        "user1": payload_user1,
        "user2": payload_user2,
        "event": payload_event,
        "client_test": app.test_client()
    }


@pytest.fixture
def gestion_user(setup_app):
    aplication = setup_app["client_test"]
    payload_user1 = setup_app["user1"]
    payload_user2 = setup_app["user2"]
    payload_event = setup_app["event"]

    aplication.post('/user/register', headers={"Content-Type": "application/json"},
                    data=payload_user1)

    aplication.post('/user/evenement', headers={"Content-Type": "application/json"},
                    data=payload_event)

    aplication.post('/user/register', headers={"Content-Type": "application/json"},
                    data=payload_user2)

    yield

    aplication.get('/user/login', headers={"Content-Type": "application/json"},
                   data=payload_user1)

    aplication.delete('/user')

    aplication.get('/user/login', headers={"Content-Type": "application/json"},
                   data=payload_user2)

    aplication.delete('/user')


def test_get_evenements(setup_app, gestion_user):
    aplication = setup_app["client_test"]

    response = aplication.get('/evenement', headers={"Content-Type": "application/json"})

    eventes = response.json['evenements']

    assert str == type(response.json['message'])
    assert dict == type(eventes)
    assert 1 == len(eventes)
    assert 200 == response.status_code


def test_get_evenement_by_id(setup_app, gestion_user):
    aplication = setup_app["client_test"]
    payload_user2 = setup_app["user2"]

    evenement = Evenement.query.filter_by(titre="Enenement de Test").first()

    id = evenement.id

    aplication.get('/user/login', headers={"Content-Type": "application/json"},
                   data=payload_user2)

    response = aplication.get('/evenement/' + str(id), headers={"Content-Type": "application/json"})

    evente = response.json['evenement']

    assert str == type(response.json['message'])
    assert dict == type(evente)
    assert 5 == len(evente)
    assert 200 == response.status_code


def test_get_evenement_by_id_error(setup_app, gestion_user):
    application = setup_app["client_test"]
    payload_user2 = setup_app["user2"]

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload_user2)

    response = application.get('/evenement/999', headers={"Content-Type": "application/json"})
    message = response.json['message']
    assert 404 == response.status_code
    assert str == type(message)
    assert "Not fond evenement for id=999" == message


def test_inscription(setup_app, gestion_user):
    application = setup_app["client_test"]
    payload_user2 = setup_app["user2"]

    evenement = Evenement.query.filter_by(titre="Enenement de Test").first()

    id = evenement.id

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload_user2)

    response = application.put('/evenement/' + str(id))
    message = response.json['message']

    assert 200 == response.status_code
    assert str == type(message)
    assert "Inscription for Evenement : " + str(id) + " is validate" == message

    evenement = Evenement.query.filter_by(titre="Enenement de Test").first()

    assert 1 == len(evenement.inscrits)


def test_desinscription_event(setup_app, gestion_user):
    application = setup_app["client_test"]
    payload_user2 = setup_app["user2"]

    evenement = Evenement.query.filter_by(titre="Enenement de Test").first()

    id = evenement.id

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload_user2)

    application.put('/evenement/' + str(id))

    response = application.delete('/evenement/' + str(id))
    message = response.json['message']

    assert 200 == response.status_code
    assert str == type(message)
    assert "Desinscription for Evenement : " + str(id) + " is validate" == message

    evenement = Evenement.query.filter_by(titre="Enenement de Test").first()

    assert 0 == len(evenement.inscrits)
