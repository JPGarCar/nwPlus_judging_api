from flask import Blueprint
from flask_restful import Api

from resources.DBTester import DBTesterResource
from resources.Grades import GradesResource
from resources.Hacker import HackerResource
from resources.JudgeMaster import JudgeMasterResource
from resources.Submission import SubmissionResource
from resources.Team import TeamResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(TeamResource, '/Team')
api.add_resource(SubmissionResource, '/Submission')
api.add_resource(HackerResource, '/Hacker')
api.add_resource(GradesResource, '/Grades')
api.add_resource(JudgeMasterResource, '/JudgeMaster')
api.add_resource(DBTesterResource, '/DBTester')
