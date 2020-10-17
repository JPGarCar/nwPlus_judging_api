from flask import request
from flask_restful import Resource
from models import db, Hacker, SubmissionSchema, Submission, TeamSchema, HackerSchema

hacker_schema = HackerSchema()


class HackerResource(Resource):
    def get(self):
        # grab email from args
        email = request.args.get('email')

        # query db using email to search for Hacker
        hacker = Hacker.query.filter_by(email=email).first()

        # check if hacker exist if not return error code
        if not hacker:
            return {'status': 'error', 'message': 'no hacker with such email found'}, 400

        hacker = hacker_schema.dump(hacker)
        return {'status': 'success', 'hacker': hacker}, 200
