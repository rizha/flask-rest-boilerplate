from flask.ext.restful import Resource, reqparse, marshal, fields

from app.users import User
from app import mongo


class Auth(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True,
                            location='json')

        data = parser.parse_args()
        user = User.generate_auth_token(data['email'], data['password'])

        if not user['status']:
            return user['data'], 401

        return user['data'], 200


class UserList(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, location='json')
        parser.add_argument('username', type=str, required=True,
                            location='json')
        parser.add_argument('password', type=str, required=True,
                            location='json')

        data = parser.parse_args()
        user = User.create_user(data['email'], data['username'],
                                data['password'])

        if not user['status']:
            return user['data'], 409

        return None, 201


class UserDetail(Resource):

    def get(self, username):
        resource_field = {
            'username': fields.String,
            'email': fields.String,
            'fullName': fields.String,
            'phone': fields.String,
            'gender': fields.String,
            'dateUpdated': fields.DateTime(dt_format='iso8601'),
            'dateCreated': fields.DateTime(dt_format='iso8601')
        }

        user = mongo.db.users.find_one({'username': username}, {'_id': 0})

        output = marshal(user, resource_field)

        return {'res': output}
