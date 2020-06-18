from datetime import datetime

from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discution_id = db.Column(db.Integer, db.ForeignKey('discution.id'))
    discution = db.relationship("Discution", back_populates="message")
    date = db.Column(db.DateTime, index=True, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
