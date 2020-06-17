from flask import request
from flask_restplus import Resource, fields

from app import api, db
from app.model.discution import Discution
from app.model.evenement import Evenement
from app.model.message import Message
from app.service.token import require_api_token
from app.service import token as token_service

ns_evenement = api.namespace('evenement', description="evenement operations")


@ns_evenement.route("")
class Evenements(Resource):
    def get(self):
        """
        return l'ensemble des events public
        et des events créée par les utilisateur que le user follow
        :return: dict
        """

        user = token_service.get_user_by_token()

        events = Evenement.query.filter_by(isprivate=False)

        if user is not None:
            for follow in user.followed:
                events_follow = Evenement.query.filter_by(author=follow)
                events = events.union(events_follow)

        res = {}

        for event in events:
            res[event.id] = {"titre": event.titre, "description": event.description, "date": str(event.date),
                             "autheur": event.author.username}
        return {"response": "SUCCESS", "message": "Get Evenements : ", "evenements": res}


@ns_evenement.route("/<int:id_evenement>")
@ns_evenement.param('id_evenement', 'The evenement ID')
class GestionEvenement(Resource):
    def get(self, id_evenement):
        """

        :param id_evenement:
        :return: dict
        """
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
        """

        :param id_evenement:
        :return:
        """
        event: Evenement = Evenement.query.get(id_evenement)
        user = token_service.get_user_by_token()

        if user is None:
            return {"response": "Error", "message": "Inscription Not autorized"}, 403

        event.inscrits.append(user)

        db.session.commit()

        return {"response": "SUCCESS", "message": "Inscription for Evenement : " + str(id_evenement) + " is validate"}

    @require_api_token
    def delete(self, id_evenement):
        event: Evenement = Evenement.query.get(id_evenement)
        user = token_service.get_user_by_token()

        if user not in event.inscrits:
            if user is None:
                return {"response": "Error", "message": "User  Not autorized"}, 403

        event.inscrits.remove(user)

        db.session.commit()

        return {"response": "SUCCESS",
                "message": "Desinscription for Evenement : " + str(id_evenement) + " is validate"}


@ns_evenement.route("/conversation/<int:id_evenement>")
class Conversation(Resource):
    def get(self, id_evenement):
        event: Evenement = Evenement.query.get(id_evenement)
        user = token_service.get_user_by_token()

        if event is None :
            return {"response": "Error", "message": "Evenement  Not Founf"}, 404

        if event.isprivate:
            if user is None or user not in event.inscrits:
                return {"response": "Error", "message": "User  Not autorized"}, 403

        discution: Discution = event.discution

        reponse = {}
        id_message = 0
        message: Message
        for message in discution.message:
            reponse[id_message] = {"author": message.author, "message": message.text, "date": str(message.date.strftime('%d/%m/%Y %H:%M:%S'))}
            id_message += 1

        return {"response": "SUCCESS",
                "message": "Discution  for Evenement : " + str(id_evenement), "discusion": reponse}

    def post(self, id_evenement):
        data = request.get_json()
        data_message = data["message"]

        event: Evenement = Evenement.query.get(id_evenement)
        user = token_service.get_user_by_token()

        message = Message(message_author=user)
        message.text = data_message

        discution: Discution = event.discution
        discution.message.append(message)

        db.session.commit()

        return {"response": "SUCCESS",
                "message": "Discution  for Evenement"}
