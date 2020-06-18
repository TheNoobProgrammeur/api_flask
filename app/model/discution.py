from sqlalchemy.orm import relationship

from app import db


class Discution(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evenemnt_id = db.Column(db.Integer, db.ForeignKey('evenement.id'))
    evenemnt = relationship("Evenement", back_populates="discution")
    message = relationship("Message", cascade="all, delete-orphan")
