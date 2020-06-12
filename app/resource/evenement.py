from flask_restplus import Resource

from app import api
from app.model.evenement import Evenement

ns_evenement = api.namespace('evenement', description="evenement operations")


@ns_evenement.route("/")
class Evenements(Resource):
    def get(self):
        events = Evenement.query.all()
        res = {}
        for event in events:
            res[event.id] = {"titre": event.titre, "description": event.description, "date": str(event.date), "autheur": event.author.username}
        return res
