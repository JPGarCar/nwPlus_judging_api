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
    team_name = db.Column(db.Text, unique=True)
    team_members = db.relationship('Hacker', backref='team', lazy=True)
    submission = db.relationship('Submission', backref='team', lazy=True, uselist=False)

    def __init__(self, team_name):
        self.team_name = team_name


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text)
    technology = db.Column(db.Integer)
    design = db.Column(db.Integer)
    functionality = db.Column(db.Integer)
    creativity = db.Column(db.Integer)
    pitch = db.Column(db.Integer)
    hacker_id = db.Column(db.Integer, db.ForeignKey('hackers.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)

    def __init__(self, comment, technology, design, functionality, creativity, pitch, **kwargs):
        submission_id = kwargs.get('submission_id', None)
        hacker_id = kwargs.get('hacker_id', None)
        obj_id = kwargs.get('id', None)
        self.comment = comment
        self.technology = technology
        self.design = design
        self.functionality = functionality
        self.creativity = creativity
        self.pitch = pitch
        self.hacker_id = hacker_id
        self.submission_id = submission_id
        self.id = obj_id


class Hacker(db.Model):
    __tablename__ = 'hackers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    grading_complete = db.Column(db.Boolean, default=False, nullable=False)
    grades = db.relationship('Grade', backref='hacker', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.grading_complete = False


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text)
    devpost_link = db.Column(db.Text)
    youtube_link = db.Column(db.Text)
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
        include_fk = True

    @post_load
    def make_user(self, data, **kwargs):
        return Grade(**data)


class HackerSchema(ma.SQLAlchemyAutoSchema):

    grades = fields.Nested(GradeSchema, many=True)

    class Meta:
        model = Hacker
        include_fk = True

    @post_load
    def make_user(self, data, **kwargs):
        return Hacker(**data)


class SubmissionSchema(ma.SQLAlchemyAutoSchema):

    grades = fields.Nested(GradeSchema, many=True)

    class Meta:
        model = Submission
        include_fk = True

    @post_load
    def make_user(self, data, **kwargs):
        return Submission(**data)


class TeamSchema(ma.SQLAlchemyAutoSchema):

    team_members = fields.Nested(HackerSchema, many=True)
    submission = fields.Nested(SubmissionSchema)

    class Meta:
        model = Team
        include_fk = True

    @post_load
    def make_user(self, data, **kwargs):
        return Team(**data)
