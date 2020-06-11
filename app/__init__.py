from flask import Flask, request
from flask_restplus import Api
from flask_login import LoginManager

from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app=app, version='0.1', title='My API', description='', validate=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app.resource import pong, user
from app.model import user
