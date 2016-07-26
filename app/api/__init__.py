from flask import Blueprint

from flask.ext.restful import Api


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from . import routes
