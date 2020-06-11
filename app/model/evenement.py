from datetime import datetime

from sqlalchemy.orm import relationship

from app import db
from app.model.tables import inscription_list


class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titer = db.Column(db.String())
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    createur = db.Column(db.Integer, db.ForeignKey('user.id'))
    inscrits = relationship("Users", secondary=inscription_list, back_populates="evenements")
