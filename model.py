import uuid

import flask_sqlalchemy

import app


db = flask_sqlalchemy.SQLAlchemy(app.app)


class Secret(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text_above = db.Column(db.Text, nullable=False)
    secret1 = db.Column(db.String(255), nullable=False)
    secret2 = db.Column(db.String(255), nullable=False)
    text_below = db.Column(db.Text, nullable=False)
    signature = db.Column(db.Text)

    @classmethod
    def create(cls):
        return cls(id=str(uuid.uuid4()))


db.create_all()
