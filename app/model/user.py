from sqlalchemy.orm import relationship

from app import db
from app.model.tables import inscription_list, followers, request_followers


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    evenements_cree = db.relationship('Evenement', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    evenements = relationship("Evenement", secondary=inscription_list, back_populates="inscrits")
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    request_follwed = db.relationship(
        'User', secondary=request_followers,
        primaryjoin=(request_followers.c.follower_id == id),
        secondaryjoin=(request_followers.c.followed_id == id),
        backref=db.backref('request_followers', lazy='dynamic'), lazy='dynamic')
    message_ecrit = db.relationship('Message', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return 'User {}'.format(self.username)
