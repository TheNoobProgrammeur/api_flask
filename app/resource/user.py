import hashlib

from flask import request, session
from flask_restplus import Resource, fields

from app import api
from app import db
from app.model.user import User
from app.service import token as token_service
from app.service.token import require_api_token

ns_user = api.namespace('user', description="user operations")

register_definition = api.model('User Informations for Register', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
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


login_definition = api.model('User Informations for Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})


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


@ns_user.route("/")
class Delete(Resource):
    @require_api_token
    def delete(self):
        token = session['api_sessions_token']

        id = token_service.get_id_by_token(token)
        user = User.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()

        del session['api_sessions_token']

        return {"response": "SUCCESS", "message": "Goodbye."}
