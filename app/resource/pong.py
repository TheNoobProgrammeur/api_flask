from flask_restplus import Resource

from app import api
from app.service.token import *

ns_books = api.namespace('ping', description="ping operations")


@ns_books.route("/")
class Pong(Resource):
    @require_api_token
    def get(self):
        return {"response": 'pong'}
