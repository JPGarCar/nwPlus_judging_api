from flask import request
from flask_restful import Resource
from models import db, Team, SubmissionSchema, Submission, TeamSchema, Hacker, HackerSchema, GradeSchema, Grade

hacker_schema = HackerSchema()
grades_schema = GradeSchema(many=True)
grade_schema = GradeSchema()


class GradesResource(Resource):
    def get(self):
        # grab hacker id from request arguments
        hacker_id = request.args.get('hacker_id')

        # search for hacker
        hacker = Hacker.query.get(hacker_id)

        if not hacker:
            return {'status': 'error', 'message': 'given hacker id does not exist'}, 400

        grades = hacker.grades

        result = grades_schema.dump(grades)
        return {'status': 'success', 'grades': result}, 200

    def post(self):
        # grab hacker id from request arguments
        hacker_id = request.args.get('hacker_id')

        # grab hacker and update grading_complete
        hacker = Hacker.query.get(hacker_id)

        if not hacker:
            return {'status': 'error', 'message': 'hacker id does not exist'}, 400

        hacker.grading_complete = True

        # grab the grades data from request json
        grades_json_data = request.get_json()

        if not grades_json_data:
            return {'status': 'error', 'message': 'no json data passed'}, 400

        # make sure the json data is a list of json data
        if not isinstance(grades_json_data, list):
            return {'status': 'error', 'message': 'expected a list of dictionaries, did not get a list'}

        # update grade rows in db by doing a session add, this works because I am also giving a primary key

        for json in grades_json_data:
            grade = grade_schema.load(json)
            Grade.query.filter_by(id=grade.id).update(json)

        db.session.commit()

        result = hacker_schema.dump(hacker)

        return {'status': 'success', 'hacker': result}, 200
