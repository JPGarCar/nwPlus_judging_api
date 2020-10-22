from flask import request
from flask_restful import Resource

from judge_master import JudgeMaster


class JudgeMasterResource(Resource):
    def post(self):
        # grab number of grades per team from args
        grades_per_project = int(request.args.get('grades_per_project'))

        if grades_per_project is None:
            return {'status': 'error', 'message': 'no argument grades_per_project given'}, 400

        judge_master = JudgeMaster()
        return judge_master.shuffle(grades_per_project)