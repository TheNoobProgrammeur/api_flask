from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey

inscription_list = Table('inscription', db.metadata,
                         Column('user_id', Integer, ForeignKey('user.id')),
                         Column('evenement_id', Integer, ForeignKey('evenement.id'))
                         )

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )

request_followers = db.Table('request_followers',
                             db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                             )
