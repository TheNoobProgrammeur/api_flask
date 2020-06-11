from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app=app, version='0.1', title='My API', description='', validate=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app.resource import pong, user
from app.model import user
