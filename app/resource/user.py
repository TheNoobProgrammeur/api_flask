import hashlib
from datetime import datetime

from flask import request, session
from flask_restplus import Resource, fields

from app import api
from app import db
from app.model.discution import Discution
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

# login_definition = api.model('User Informations for Login', {
#     'username': fields.String(required=True, description="Username"),
#     'password': fields.String(required=True, description="User password")
# })

evenement_definition = api.model('Evenements Informations for creation', {
    'titre': fields.String(required=True, description="Titre for new event"),
    'date': fields.DateTime(required=True, description="Event day"),
    'description': fields.String,
    'isPrivate': fields.Boolean(default=False)
})

body_delete_event = api.model('Param for delete Evenement', {
    'id_event': fields.Integer(required=True, description="Event id for delete")
})


@ns_user.route("/register")
class Register(Resource):
    @api.expect(register_definition)
    def post(self):
        """
        Enregistre un utilisateur
        :return:
        """
        data = request.get_json()

        user = User()
        user.username = data.get("username")
        user.email = data.get("email")

        password: str = data.get("password")

        user.password_hash = hashlib.sha256(password.encode("UTF-8")).hexdigest()

        db.session.add(user)
        db.session.commit()

        rep = token_service.encode_auth_token(user.id).decode("utf-8")
        session['api_sessions_token'] = rep

        return {"response": "SUCCESS", "message": "Your is resisted", "token": rep}


@ns_user.route("/login")
class Login(Resource):
    @api.expect(login_definition)
    def get(self):
        """
        Permet a un utilisateur de s'identifier
        :return:
        """

        data = request.get_json()

        username = data.get("username")
        password: str = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user is None or hashlib.sha256(password.encode("UTF-8")).hexdigest() != user.password_hash:
            return {"response": "ERROR : user or login incorrect"}, 403
        else:
            rep = token_service.encode_auth_token(user.id).decode("utf-8")
            session['api_sessions_token'] = rep
            return {"response": "SUCCESS", "message": "Your is identified", "token": rep}


@ns_user.route("/logout")
class Logout(Resource):
    @require_api_token
    def get(self):
        """
        Permet a un utilisateur de ce déconnecter
        :return:
        """
        del session['api_sessions_token']
        return {"response": "SUCCESS", "message": "Your session is delete"}


@ns_user.route("")
class Delete(Resource):
    @require_api_token
    def delete(self):
        """
        Permet de suprimer son compte
        :return:
        """
        user = token_service.get_user_by_token()
        db.session.delete(user)
        db.session.commit()
        del session['api_sessions_token']
        return {"response": "SUCCESS", "message": "Goodbye."}


@ns_user.route("")
class GestionUser(Resource):
    @require_api_token
    def get(self):
        """
        Return son profil utilisateur
        :return:
        """
        user = token_service.get_user_by_token()
        evenements = user.evenements_cree
        evenement_follow = user.evenements
        followeds = user.followed
        profile = {"username": user.username, "email": user.email}

        indice = 0
        profile["evenements"] = {}
        for event in evenements:
            profile["evenements"][indice] = {"id": event.id, "titre": event.titre, "description": event.description,
                                             "date": str(event.date)}
            indice += 1

        indice = 0
        profile["followEvent"] = {}
        for event in evenement_follow:
            profile["followEvent"][indice] = {"id": event.id, "titre": event.titre, "description": event.description,
                                              "date": str(event.date), "autheur": event.author.username}
            indice += 1

        indice = 0
        profile["amies"] = {}
        for followed in followeds:
            profile["amies"][indice] = {"username": followed.username}

        return {"response": "SUCCESS", "message": "Your profile", "profile": profile}


@ns_user.route("/evenement")
class GestionEvenement(Resource):
    @require_api_token
    def get(self):
        """
        Return les evenelents que l'utilisateur a créée
        :return:
        """
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
        """
        Permet a un utilisateur de créée un evenement
        :return:
        """
        data = request.get_json()

        user = token_service.get_user_by_token()

        evenement = Evenement(author=user)
        evenement.titre = data["titre"]
        evt_date = data["date"]
        evenement.date = datetime.strptime(evt_date, '%d/%m/%Y %H:%M')
        if "description" in data:
            evenement.description = data["description"]

        if "isPrivate" in data:
            evenement.isprivate = data["isPrivate"]

        db.session.add(evenement)

        discution = Discution(evenemnt=evenement)

        db.session.add(discution)

        db.session.commit()

        return {"response": "SUCCESS", "message": "Evenement is created"}

    @require_api_token
    @api.expect(body_delete_event)
    def delete(self):
        """
        Permet a un utilisateur de suprimmer un evenement
        :return:
        """
        data = request.get_json()

        id_event = data["id_event"]

        user = token_service.get_user_by_token()

        evenement = user.evenements_cree.filter_by(id=id_event).first()

        db.session.delete(evenement)
        db.session.commit()

        return {"response": "SUCCESS", "message": "Evenement is delete"}


@ns_user.route("/follower")
class Follower(Resource):
    @require_api_token
    def get(self):
        """
        Return les users que le user courant follow
        :return:
        """
        user = token_service.get_user_by_token()

        followeds = user.followed

        indice = 0
        follow = {}
        for followed in followeds:
            follow[indice] = {"username": followed.username}

        return {"response": "SUCCESS", "message": "You follow", "followeds": follow}


@ns_user.route("/follower/<int:id_user>")
class GestionFollower(Resource):
    @require_api_token
    def post(self, id_user):
        user = token_service.get_user_by_token()
        user_followed: User = User.query.get(id_user)

        user_followed.request_follwed.append(user)
        db.session.commit()

        return {"response": "SUCCESS", "message": "Request follow user " + str(id_user)}


@ns_user.route("/follower/accept/<int:id_user>")
class AcceptationFollower(Resource):
    @require_api_token
    def post(self, id_user):
        user: User = token_service.get_user_by_token()
        user_follower: User = User.query.get(id_user)

        if user_follower in user.request_follwed:
            user_follower.followed.append(user)
            user.request_follwed.remove(user_follower)

            db.session.commit()

        return {"response": "SUCCESS", "message": "You accept request follow user " + str(id_user)}
