from flask import Blueprint
from flask_restful import Api
from resources.Team import TeamResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(TeamResource, '/Team')

