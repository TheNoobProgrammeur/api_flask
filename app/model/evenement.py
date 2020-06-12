from datetime import datetime

from sqlalchemy.orm import relationship

from app import db
from app.model.tables import inscription_list


class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, index=True, default=datetime.now().strftime('%d-%m-%Y %H:%M'))
    createur = db.Column(db.Integer, db.ForeignKey('user.id'))
    inscrits = relationship("User", secondary=inscription_list, back_populates="evenements")
