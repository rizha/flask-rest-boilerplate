from app import mongo


class Article:

    def create(self, title, description):
        mongo.db.post.insert_one({'title': title,
                                  'descripition': description})
