from sqlalchemy.orm import relationship

from app import db
from app.model.tables import inscription_list


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    evenements_cree = db.relationship('Evenement', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    evenements = relationship("Evenement", secondary=inscription_list, back_populates="inscrits")

    def __repr__(self):
        return 'User {}'.format(self.username)
