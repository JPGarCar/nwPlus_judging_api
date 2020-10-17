from flask import request
from flask_restful import Resource
from models import db, Team, TeamSchema, Submission

team_schema = TeamSchema()


class TeamResource(Resource):
    def get(self):
        # Query Team from db using request team_id
        team_id = request.args.get('team_id')
        team = Team.query.get(team_id)

        # Check if team exist if not return 400 error code
        if not team:
            return {'status': 'error', 'message': 'team id is non existent'}, 400

        # list of possible grades available to send
        grades = team.submission.grades

        # Check if at least one team member has finished their grading
        # TODO

        team = team_schema.dump(team)
        return {'status': 'success', 'team': team, 'grades': grades}, 200
