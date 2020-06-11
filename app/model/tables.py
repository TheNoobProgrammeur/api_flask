from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey

inscription_list = Table('inscription', db.metadata,
                         Column('user_id', Integer, ForeignKey('user.id')),
                         Column('evenement_id', Integer, ForeignKey('evenement.id'))
                         )