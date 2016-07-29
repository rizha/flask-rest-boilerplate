from flask_restful import Resource, reqparse

from app.users import User


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

        return {'message': 'success'}, 201

    def get(self):
        users = User.get_all_user()

        return users, 200


class UserDetail(Resource):

    def get(self, username):

        user = User.get_user(username)

        if not user:
            return user['data'], 404
        return user['data'], 200
