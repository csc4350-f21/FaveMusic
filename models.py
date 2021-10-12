from flask_login import UserMixin
from . import db

# from sqlalchemy import ForeignKey


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    artistids = db.relationship("ArtistID")


class ArtistID(UserMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    artistid = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    artistname = db.Column(db.String(100), nullable=False)
