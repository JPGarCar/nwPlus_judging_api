from flask import request
from flask_restful import Resource

from models import Team, Submission, Hacker, db, Grade


class DBTesterResource(Resource):
    def post(self):
        # grab argument to know what operation we want
        operation = request.args.get('operation')
        try:
            amount = int(request.args.get('amount'))
        except:
            return {'status': 'error', 'message': 'amount arg needs to be an int'}, 400

        if not (amount or operation):
            return {'status': 'error', 'message': 'no operation or amount argument given'}, 400

        if operation == 'delete all':
            Team.query.delete()
            Submission.query.delete()
            Hacker.query.delete()
            Grade.query.delete()
            db.session.commit()
            return {'status': 'success'}, 200

        if operation == 'single full build':
            for index in range(amount):
                # create team
                team = Team('Team number {}'.format(index))
                submission = Submission('this is a description', 'this is a devpost link', 'this is a youtube link')
                team.submission = submission
                # create hacker
                hacker = Hacker('hacker name {}'.format(index), 'email{}@gmail.com'.format(index))
                team.team_members.append(hacker)

                # add new objects to db
                db.session.add(team)
            db.session.commit()
            return {'status': 'success'}, 200

        if operation == 'multi full build':
            # grab second amount
            try:
                second_amount = int(request.args.get('second_amount'))
            except:
                return {'status': 'error', 'message': 'second_amount arg needs to be an int'}, 400
            if not second_amount:
                return {'status': 'error', 'message': 'no second_amount argument given for multi operation'}, 400

            for index in range(amount):
                # create team
                team = Team('Team number {}'.format(index))
                submission = Submission('this is a description', 'this is a devpost link', 'this is a youtube link')
                team.submission = submission
                # create hacker
                for num in range(second_amount):
                    hacker = Hacker('hacker name {} - {}'.format(index, num), 'email{}_{}@gmail.com'.format(index, num))
                    team.team_members.append(hacker)

                # add new objects to db
                db.session.add(team)
            db.session.commit()
            return {'status': 'success'}, 200
