import hashlib
from datetime import datetime

from flask import request, session
from flask_restplus import Resource, fields

from app import api
from app import db
from app.model.evenement import Evenement
from app.model.user import User
from app.service import token as token_service
from app.service.token import require_api_token

ns_user = api.namespace('user', description="user operations")

register_definition = api.model('User Informations for Register', {
    'username': fields.String(required=True, description="Username"),
    'email': fields.String(required=True, description="User email"),
    'password': fields.String(required=True, description="User password")
})


login_definition = api.model('User Informations for Login', {
    'username': fields.String(required=True, description="Username"),
    'password': fields.String(required=True, description="User password")
})

evenement_definition = api.model('Evenements Informations for creation', {
    'titre': fields.String(required=True, description="Titre for new event"),
    'date': fields.DateTime(required=True, description="Event day"),
    'description': fields.String
})

body_delete_event = api.model('Param for delete Evenement', {
    'id_event': fields.Integer(required=True, description="Event id for delete")
})


@ns_user.route("/register")
class Register(Resource):
    @api.expect(register_definition)
    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return data, 404
        else:
            user = User()
            user.username = data.get("username")
            user.email = data.get("email")

            password: str = data.get("password")

            user.password_hash = hashlib.sha256(password.encode("UTF-8")).hexdigest()

            db.session.add(user)
            db.session.commit()

            rep = token_service.encode_auth_token(user.id)
            session['api_sessions_token'] = rep

            return {"response": "SUCCESS", "message": "Your is resisted"}


@ns_user.route("/login")
class Login(Resource):
    @api.expect(login_definition)
    def get(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return data, 404

        username = data.get("username")
        password: str = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user is None or hashlib.sha256(password.encode("UTF-8")).hexdigest() != user.password_hash:
            return {"response": "ERROR : user or login incorrect"}, 403
        else:
            rep = token_service.encode_auth_token(user.id)
            session['api_sessions_token'] = rep
            return {"response": "SUCCESS", "message": "Your is identified"}


@ns_user.route("/logout")
class Logout(Resource):
    @require_api_token
    def get(self):
        del session['api_sessions_token']
        return {"response": "SUCCESS", "message": "Your session is delete"}


@ns_user.route("")
class Delete(Resource):
    @require_api_token
    def delete(self):
        user = token_service.get_user_by_token()
        db.session.delete(user)
        db.session.commit()
        del session['api_sessions_token']
        return {"response": "SUCCESS", "message": "Goodbye."}


@ns_user.route("/evenement")
class GestionEvenement(Resource):
    @require_api_token
    def get(self):
        user = token_service.get_user_by_token()

        evenements = user.evenements_cree

        res = {}
        indice = 0
        for event in evenements:
            res[indice] = {"id": event.id, "titre": event.titre, "description": event.description,
                           "date": str(event.date),
                           "autheur": event.author.username}
            indice += 1

        return {"response": "SUCCESS", "message": "Liste des evenement.", "evenements": res}

    @require_api_token
    @api.expect(evenement_definition)
    def post(self):
        data = request.get_json()

        user = token_service.get_user_by_token()

        evenement = Evenement(author=user)
        evenement.titre = data["titre"]
        evt_date = data["date"]
        evenement.date = datetime.strptime(evt_date, '%d/%m/%Y %H:%M')
        evenement.description = data["description"]

        db.session.add(evenement)
        db.session.commit()

        return {"response": "SUCCESS", "message": "Evenement is created"}

    @require_api_token
    @api.expect(body_delete_event)
    def delete(self):
        data = request.get_json()

        id_event = data["id_event"]

        user = token_service.get_user_by_token()

        evenement = user.evenements_cree.filter_by(id=id_event).first()

        db.session.delete(evenement)
        db.session.commit()

        return {"response": "SUCCESS", "message": "Evenement is delete"}
