from datetime import datetime
from collections import OrderedDict

from flask import current_app as app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash

from app import mongo


class User:

    @staticmethod
    def generate_auth_token(email, password):
        user = mongo.db.users.find_one({'email': email},
                                       {'password': password})

        # No email found
        if not user:
            return {
                'status': False,
                'data': {
                    'message': {
                        'email': 'User "{}" is not registered.'.format(email)
                    }
                }
            }

        # Password does not match
        if not check_password_hash(user['password'], password):
            return {
                'status': False,
                'data': {
                    'message': {
                        'password': 'Password does not match.'
                    }
                }
            }

        s = Serializer(app.config['SECRET_KEY'],
                       expires_in=app.config['TOKEN_EXPIRATION'])
        return {
            'status': True,
            'data': {
                'token': s.dumps({'user_id': str(user['_id'])}).decode('utf-8')
            }
        }

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            s.loads(token)
        except SignatureExpired:
            return False  # valid token, but expired
        except BadSignature:
            return False  # invalid token
        return True

    @staticmethod
    def create_user(email, username, password):
        password_hash = generate_password_hash(password)

        # find user by email
        user = mongo.db.users.find_one({'email': email})

        if user:
            return {
                'status': False,
                'data': {
                    'message': {
                        'email': 'Email already registered.'
                    }
                }
            }

        # find user by username
        user = mongo.db.users.find_one({'username': username})

        if user:
            return {
                'status': False,
                'data': {
                    'message': {
                        'username': 'Username already taken.'
                    }
                }
            }

        data = OrderedDict([
            ('email', email),
            ('username', username),
            ('password', password_hash),
            ('fullName', None),
            ('phone', None),
            ('gender', None),
            ('role', None),
            ('dateUpdated', None),
            ('dateCreated', datetime.utcnow())
        ])

        user = mongo.db.users.insert_one(data)

        if user:
            return {'status': True}

    @staticmethod
    def get_user(username):

        user = app.cache.get('username')

        if not user:
            user = mongo.db.users.find_one({'username': username}, {'_id': 0})

            if not user:
                return {
                    'status': False,
                    'data': {'message': "User does not exists"}
                }

            app.cache.set('username', user)

        user['dateCreated'] = user['dateCreated'].isoformat()
        user['dateUpdated'] = user['dateUpdated'].isoformat() \
            if user['dateUpdated'] else None

        return {
            'status': True,
            'data': user
        }

    @staticmethod
    def get_all_user():

        users = []
        for user in mongo.db.users.find({}, {"_id": 0}):
            user['dateCreated'] = user['dateCreated'].isoformat()
            user['dateUpdated'] = user['dateUpdated'].isoformat() \
                if user['dateUpdated'] else None
            users.append(user)

        return users
