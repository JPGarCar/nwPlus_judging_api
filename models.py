from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String, unique=True)

    # TODO add all other fields

    def __init__(self, teamName):
        self.teamName = teamName


class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_fk = True
