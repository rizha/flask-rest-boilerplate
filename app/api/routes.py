from . import api
from .resources import *


"""
User route
"""
api.add_resource(Auth, '/auth')
api.add_resource(UserDetail, '/users/<username>')
api.add_resource(UserList, '/users')
