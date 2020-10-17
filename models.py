from flask import Flask
from marshmallow import Schema, fields, pre_load, validate, post_load
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


# Models


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String, unique=True)
    hackers = db.relationship('Hacker', backref='team', lazy=True)
    submission = db.relationship('Submission', backref='team', lazy=True, uselist=False)

    def __init__(self, team_name):
        self.team_name = team_name


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
    grading_complete = db.Column(db.Boolean)
    grades = db.relationship('Grade', backref='hacker', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.grading_complete = False


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    devpost_link = db.Column(db.String)
    youtube_link = db.Column(db.String)
    grades = db.relationship('Grade', backref='submission', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def __init__(self, description, devpost_link, youtube_link):
        self.description = description
        self.devpost_link = devpost_link
        self.youtube_link = youtube_link


# Schemas

class GradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grade

    @post_load
    def make_user(self, data, **kwargs):
        return Grade(**data)


class HackerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hacker

    @post_load
    def make_user(self, data, **kwargs):
        return Hacker(**data)


class SubmissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Submission

    @post_load
    def make_user(self, data, **kwargs):
        return Submission(**data)


class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_fk = True

    @post_load
    def make_user(self, data, **kwargs):
        return Team(**data)
