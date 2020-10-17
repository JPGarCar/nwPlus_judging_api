from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from models import db, Hacker, Team, HackerSchema

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

    def post(self):
        # grab data from json
        json_data = request.get_json(force=True)

        # check if team id is a real team id
        team = Team.query.get(json_data['team_id'])

        if not team:
            return {'status': 'error', 'message': 'given team id does not match any teams'}, 400

        # isolate hacker data and create object
        hacker_json_data = json_data.copy()
        del hacker_json_data['team_id']

        input_hacker = hacker_schema.load(hacker_json_data)

        # check if there is a hacker with the same email
        hacker = Hacker.query.filter_by(email=input_hacker.email).first()

        if hacker:
            return {'status': 'error', 'message': 'a hacker with that email already exists'}, 400

        team.team_members.append(input_hacker)
        # db.session.add(team)
        # db.session.add(input_hacker)
        db.session.commit()

        result = hacker_schema.dump(input_hacker)

        return {'status': 'success', 'hacker': result}, 200