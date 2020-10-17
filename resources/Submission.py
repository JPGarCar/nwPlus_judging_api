from flask import request
from flask_restful import Resource
from models import db, Team, SubmissionSchema, Submission, TeamSchema

submission_schema = SubmissionSchema()
team_schema = TeamSchema()


class SubmissionResource(Resource):
    def post(self):
        # grab data from json input
        submission_json_data = request.get_json(force=True)
        if not submission_json_data:
            return {'status': 'error', 'message': 'No input data provided'}, 400

        # separate input json into two, one for team, one for submission
        team_json_data = {
            "team_name": request.args.get('team_name')
        }

        input_submission = submission_schema.load(submission_json_data)
        input_team = team_schema.load(team_json_data)

        # add submission to the team
        input_team.submission = input_submission

        # make sure the team name is unique
        team = Team.query.filter_by(team_name=input_team.team_name).first()
        if team:
            return {'message': 'Team name already exists'}, 400
        else:
            db.session.add(input_team)
            db.session.commit()

        result = team_schema.dump(input_team)

        return {'status': 'success', 'data': result}, 201
