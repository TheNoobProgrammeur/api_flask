import json

import pytest

from app import app
from app.model.evenement import Evenement
from app.model.user import User


@pytest.fixture
def setup_app():
    application = app.test_client()

    username2 = "antoine_test2"
    password2 = "azerty2"
    email2 = "test2@test.ts"

    payload_user2 = json.dumps({
        "username": username2,
        "email": email2,
        "password": password2
    })

    return {
        "user2": payload_user2,
        "client_test": application
    }


@pytest.fixture
def gestion_user(setup_app):
    aplication = setup_app["client_test"]
    payload_user2 = setup_app["user2"]

    aplication.post('/user/register', headers={"Content-Type": "application/json"},
                    data=payload_user2)

    yield

    aplication.get('/user/login', headers={"Content-Type": "application/json"},
                   data=payload_user2)

    aplication.delete('/user')


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


def test_login_error_no_data(setup_app):
    application = setup_app["client_test"]

    response = application.get('/user/login')

    assert 400 == response.status_code


def test_login_error_password(setup_app):
    application = setup_app["client_test"]

    username = "antoine_test"
    password = "password_error"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    response = application.get('/user/login', headers={"Content-Type": "application/json"},
                               data=payload)

    assert 403 == response.status_code
    assert "ERROR : user or login incorrect" == response.json["response"]


def test_login_error_username(setup_app):
    application = setup_app["client_test"]

    username = "username_error"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    response = application.get('/user/login', headers={"Content-Type": "application/json"},
                               data=payload)

    assert 403 == response.status_code
    assert "ERROR : user or login incorrect" == response.json["response"]


def test_see_profile(setup_app):
    application = setup_app["client_test"]

    username = "antoine_test"
    password = "azerty"
    email = "test@test.gouv"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload)

    response = application.get('/user')

    profile = response.json['profile']

    assert 200 == response.status_code
    assert dict == type(profile)
    assert username == profile["username"]
    assert email == profile["email"]


def test_create_event(setup_app):
    application = setup_app["client_test"]

    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    application.get('/user/login', headers={"Content-Type": "application/json"},
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


def test_get_event(setup_app):
    application = setup_app["client_test"]

    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    titre_event = "Enenement de Test"
    date_event = '2020-08-11 12:30:00'
    description = "Test de creation event"

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload)

    response = application.get('/user/evenement')

    assert dict == type(response.json['evenements'])

    event = response.json['evenements']["0"]

    assert titre_event == event["titre"]
    assert description == event["description"]
    assert date_event == event["date"]
    assert username == event["autheur"]

    assert 200 == response.status_code


def test_delete_event(setup_app):
    application = setup_app["client_test"]

    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    evenement = Evenement.query.filter_by(titre="Enenement de Test").first()

    id = evenement.id

    payload_idEvent = json.dumps({
        "id_event": id
    })

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload)

    response = application.delete('/user/evenement', headers={"Content-Type": "application/json"},
                                  data=payload_idEvent)

    assert 200 == response.status_code
    assert str == type(response.json['message'])
    assert "Evenement is delete" == response.json['message']


def test_follower_user(setup_app,gestion_user):
    application = setup_app["client_test"]
    user_follow = User.query.filter_by(username="antoine_test2").first()
    id = user_follow.id

    response = application.post('/user/follower/'+str(id))

    assert 200 == response.status_code


def test_accept_request_follwed(setup_app,gestion_user):
    application = setup_app["client_test"]
    payload = setup_app["user2"]
    user_follow = User.query.filter_by(username="antoine_test2").first()
    id_user2 = user_follow.id

    user = User.query.filter_by(username="antoine_test").first()
    id_user1 = user.id

    application.post('/user/follower/' + str(id_user2))
    application.get('/user/logout')
    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload)
    response = application.post('/user/follower/accept/' + str(id_user1))
    assert 200 == response.status_code



def test_logout(setup_app):
    application = setup_app["client_test"]

    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload)

    response = application.get('/user/logout')

    assert 200 == response.status_code

    response = application.get('/ping')

    assert 403 == response.status_code


def test_delete(setup_app):
    application = setup_app["client_test"]

    username = "antoine_test"
    password = "azerty"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    application.get('/user/login', headers={"Content-Type": "application/json"},
                    data=payload)

    user = User.query.filter_by(username=username).first()
    id_event = 0
    for event in user.evenements_cree:
        id_event = event.id

    payload = json.dumps({
        "id_event": id_event
    })

    response = application.delete('/user', headers={"Content-Type": "application/json"},
                                  data=payload)
    assert 200 == response.status_code
    assert str == type(response.json['message'])
    assert "Goodbye." == response.json['message']
