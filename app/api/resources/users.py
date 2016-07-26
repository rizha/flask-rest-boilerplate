from flask.ext.restful import Resource, reqparse

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
