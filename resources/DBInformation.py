from flask import request
from flask_restful import Resource
from models import db, Team, SubmissionSchema, Submission, TeamSchema, Hacker, HackerSchema, GradeSchema, Grade


class DBInformationResource(Resource):
    def get(self):
        # general db numbers
        return_value = {
            'status': 'success',
            'number_of_hackers': Hacker.query.count(),
            'number_of_teams': Team.query.count(),
            'number_of_submissions': Submission.query.count(),
            'number_of_grades': Grade.query.count(),
        }

        # if grades available, number completed
        if Grade.query.count() != 0:
            return_value['number_of_finished_grades'] = Grade.query.filter(Grade.technology.isnot(None)).count()
            return_value['number_of_remaining_grades'] = Grade.query.filter(Grade.technology.is_(None)).count()
            return_value['number_of_finished_hackers'] = Hacker.query.filter(Hacker.grading_complete.is_(True)).count()

        return return_value, 200
