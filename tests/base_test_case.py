import unittest

import httpretty
from app import create_app, mongo


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            self.mongo = mongo

        httpretty.enable()

    def tearDown(self):
        pass
