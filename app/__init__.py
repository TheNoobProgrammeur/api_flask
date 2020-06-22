from flask import Flask
from flask_migrate import Migrate
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app=app, version='1.0', title='API Evenement', description="API de gestion d'événements", validate=True)
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.resource import pong, user, evenement
from app.model import user, evenement, message, discution
