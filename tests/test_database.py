from tests import BaseTestCase


class DatabaseTestCase(BaseTestCase):

    def setUp(self):
        """
        Create todo collections
        """
        super(DatabaseTestCase, self).setUp()

        with self.app.app_context():
            self.mongo.db.todo.insert_one({
                'title': 'Whatever you want',
                'text': 'Do what the fuck you wanna do bitch!'
            })

    def test_todo_query(self):
        """
        check query
        """
        with self.app.app_context():
            todo = self.mongo.db.todo.find_one()
        self.assertTrue('Whatever' in todo['title'])

