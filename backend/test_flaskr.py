import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        self.database_name = 'trivia_test'
        self.database_username = 'postgres'
        self.database_password = '2098'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_username, self.database_password, 'localhost:5432', self.database_name)
        
        setup_db(self.app, self.database_path)
        
        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["real_total"])
        self.assertTrue(data["paginated_total"])
        self.assertTrue(data["current_page"])
        self.assertTrue(len(data["categories"]))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()