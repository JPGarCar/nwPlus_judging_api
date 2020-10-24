from flask import request
from flask_restful import Resource

from judge_master import JudgeMaster


class JudgeMasterResource(Resource):
    def post(self):
        # grab number of grades per team from args
        try:
            grades_per_project = int(request.args.get('grades_per_project'))
        except:
            return {'status': 'error', 'message': 'argument grades_per_project is not an int'}, 400

        if grades_per_project is None:
            return {'status': 'error', 'message': 'no argument grades_per_project given'}, 400

        judge_master = JudgeMaster()
        distribution = judge_master.shuffle(grades_per_project)
        return {'status': 'success', 'distribution': distribution}, 200

    def get(self):
        # get number of grades per hacker
        try:
            grades_per_hacker = int(request.args.get('grades_per_hacker'))
        except:
            return {'status': 'error', 'message': 'argument grades_per_hacker is not an int'}, 400
        if not grades_per_hacker:
            return {'status': 'error', 'message': 'no argument grades_per_hacker given'}, 400

        judge_master = JudgeMaster()
        grades_per_submission = judge_master.getOptimalGradesPerSubmission(grades_per_hacker)
        return {'status': 'success', 'data': 'when looking for {} grades per hacker, {} grades per project is the optimal value'.format(grades_per_hacker, grades_per_submission)}, 200