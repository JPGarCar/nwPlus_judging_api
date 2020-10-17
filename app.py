from flask import Blueprint
from flask_restful import Api

from resources.Grades import GradesResource
from resources.Hacker import HackerResource
from resources.Submission import SubmissionResource
from resources.Team import TeamResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(TeamResource, '/Team')
api.add_resource(SubmissionResource, '/Submission')
api.add_resource(HackerResource, '/Hacker')
api.add_resource(GradesResource, '/Grades')
