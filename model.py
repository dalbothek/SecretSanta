import uuid
import json
import datetime

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


class AuditLog(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    event = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.utcnow)

    @classmethod
    def create(cls, event, details):
        return cls(
            id=str(uuid.uuid4()),
            event=event,
            details=json.dumps(cls._fix_date_keys(details))
        )

    @classmethod
    def _fix_date_keys(cls, obj):
        if isinstance(obj, dict):
            return dict(
                (cls._fix_date_keys(key), cls._fix_date_keys(value))
                for key, value in obj.items()
            )

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        return obj


db.create_all()
