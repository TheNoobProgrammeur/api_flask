from flask_restplus import Resource

from app import api
from app.service.token import *

ns_pong = api.namespace('ping', description="ping operations")


@ns_pong.route("/")
class Pong(Resource):
    @require_api_token
    def get(self):
        return {"response": 'pong'}


@ns_pong.route("/smoke")
class Smoke(Resource):
    def get(self):
        return {"response": 'yes man'}
