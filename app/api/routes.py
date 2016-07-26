from . import api
from .resources import *


"""
User route
"""
api.add_resource(Auth, '/auth')