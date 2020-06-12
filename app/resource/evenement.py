from flask_restplus import Resource

from app import api, db
from app.model.evenement import Evenement
from app.service.token import require_api_token, get_user_by_token

ns_evenement = api.namespace('evenement', description="evenement operations")


@ns_evenement.route("")
class Evenements(Resource):
    def get(self):
        events = Evenement.query.all()
        res = {}

        for event in events:
            res[event.id] = {"titre": event.titre, "description": event.description, "date": str(event.date),

                             "autheur": event.author.username}
        return {"response": "SUCCESS", "message": "Get Evenements : ", "evenements": res}


@ns_evenement.route("/<int:id_evenement>")
class GestionEvenement(Resource):
    def get(self, id_evenement):
        event: Evenement = Evenement.query.get(id_evenement)

        if event is None:
            data = {"response": "ERROR", "message": "Not fond evenement for id=" + str(id_evenement)}
            return data, 404

        list_inscrit = {}
        i = 0
        for inscrit in event.inscrits:
            list_inscrit[i] = str(inscrit)
            i += 1

        evenement = {"titre": event.titre, "description": event.description, "date": str(event.date),
                     "autheur": event.author.username, "inscrit": list_inscrit}

        return {"response": "SUCCESS", "message": "Get Evenement : " + str(id_evenement),
                "evenement": evenement}

    @require_api_token
    def put(self, id_evenement):
        event: Evenement = Evenement.query.get(id_evenement)
        user = get_user_by_token()

        if user is None:
            return {"response": "Error", "message": "Inscription Not autorized"}

        event.inscrits.append(user)

        db.session.commit()

        return {"response": "SUCCESS", "message": "Inscription for Evenement : " + str(id_evenement) + " is validate"}
