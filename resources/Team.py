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
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        input_team = team_schema.load(json_data)

        # validate and deseiralize input
        team = Team.query.filter_by(teamName=input_team.teamName).first()
        if team:
            return {'message': 'Team already exists'}, 400
        else:
            db.session.add(input_team)
            db.session.commit()

        result = team_schema.dump(input_team)

        return {'status': 'success', 'data': result}, 201
