from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


# Models


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teamName = db.Column(db.String, unique=True)
    hackers = db.relationship('Hacker', backref='team', lazy=True)
    submission = db.relationship('Submission', backref='team', lazy=True, uselist=False)

    def __init__(self, teamName):
        self.teamName = teamName


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String)
    technology = db.Column(db.Integer)
    design = db.Column(db.Integer)
    functionality = db.Column(db.Integer)
    creativity = db.Column(db.Integer)
    pitch = db.Column(db.Integer)
    hacker_id = db.Column(db.Integer, db.ForeignKey('hackers.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)

    def __init__(self, comment, technology, design, functionality, creativity, pitch):
        self.comment = comment
        self.technology = technology
        self.design = design
        self.functionality = functionality
        self.creativity = creativity
        self.pitch = pitch


class Hacker(db.Model):
    __tablename__ = 'hackers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    judgingComplete = db.Column(db.Boolean)
    grades = db.relationship('Grade', backref='hacker', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.judgingComplete = False


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    devpostLink = db.Column(db.String)
    youtubeLink = db.Column(db.String)
    grades = db.relationship('Grade', backref='submission', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def __init__(self, description, devpostLink, youtubeLink):
        self.description = description
        self.devpostLink = devpostLink
        self.youtubeLink = youtubeLink


# Schemas

class GradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grade


class HackerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hacker


class SubmissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Submission


class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_fk = True
