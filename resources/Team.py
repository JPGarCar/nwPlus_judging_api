from flask import request
from flask_restful import Resource
from models import db, Team, TeamSchema

teams_schema = TeamSchema(many=True)
team_schema = TeamSchema()


class TeamResource(Resource):
    def get(self):
        teams = Team.query.all()
        teams = teams_schema.dump(teams)
        return {'status': 'success', 'data': teams}, 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # validate and deseiralize input
        data, errors = team_schema.load(json_data)
        if errors:
            return errors, 422
        team = Team.query.filter_by(teamName=data['teamName']).first()
        if team:
            return {'message': 'Team already exists'}, 400
        team = Team(teamName=data['teamName'])

        db.session.add(team)
        db.session.commit()

        result = team_schema.dump(team)

        return {'status': 'success', 'data': result}, 201