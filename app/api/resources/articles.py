from flask_restful import Resource, reqparse

from app.blog import Article


class ArticleList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, location='json')
        parser.add_argument('description', type=str, required=True,
                            location='json')

        data = parser.parse_args()
        user = Article.create(data['title'], data['description'])

        return user['data'], 200
