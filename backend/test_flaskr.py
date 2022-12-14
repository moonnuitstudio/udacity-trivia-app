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
        
        self.new_question = {
            "question": "What year was the Mona Lisa painted?",
            "answer": "1503",
            "difficulty": 3,
        }
        
        self.bad_new_question = {
            "question": "What year was the Mona Lisa painted?",
            "answer": "1503",
            "difficulty": "asd",
        }
        
        self.play_body = {
            "former_questions": [20,22],
            "category_id": 1
        }

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
        
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["real_total"])
        self.assertTrue(data["paginated_total"])
        self.assertTrue(data["current_page"])
        self.assertTrue(len(data["questions"]))
        
    def test_get_paginated_questions_by_category(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["real_total"])
        self.assertTrue(data["paginated_total"])
        self.assertTrue(data["current_page"])
        self.assertTrue(len(data["questions"]))
        
    def test_get_category(self):
        res = self.client().get("/categories/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["category"]))
        
    def test_get_question(self):
        res = self.client().get("/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["question"]))
        
    def test_get_categories_search(self):
        res = self.client().post("/categories", json={"search": "ar"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["real_total"])
        self.assertTrue(data["paginated_total"])
        self.assertTrue(data["current_page"])
        self.assertTrue(len(data["categories"]))
        
    def test_get_questions_search_without_results(self):
        res = self.client().post("/questions", json={"search": "asdasfdsf"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["real_total"], 0)
        self.assertEqual(data["paginated_total"], 0)
        self.assertTrue(data["current_page"])
        self.assertEqual(len(data["questions"]), 0)
        
    def test_new_question(self):
        res = self.client().post("/categories/1/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["real_total"])
        self.assertTrue(data["paginated_total"])
        self.assertTrue(data["current_page"])
        self.assertTrue(len(data["questions"]))
        
    def test_delete_question(self):
        res = self.client().delete("/questions/10")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["real_total"])
        self.assertTrue(data["paginated_total"])
        self.assertTrue(data["current_page"])
        self.assertTrue(len(data["questions"]))
        
    def test_404_if_category_does_not_exist(self):
        res = self.client().get("/categories/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
        
    def test_questions_play(self):
        res = self.client().post("/questions/play", json=self.play_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["former_questions"])
        self.assertTrue(data["question"])
        
    def test_400_if_difficulty_is_text(self):
        res = self.client().post("/categories/2/questions", json=self.bad_new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()