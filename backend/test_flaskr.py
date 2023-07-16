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
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres', 'abc', 'localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        self.new_question = {            
            "question": 'question',
            "answer": 'answer',
            "category": 3,
            "difficulty": 5
        }

        # binds the app to the current context
        with self.app.app_context():
            try:
                self.db = SQLAlchemy()
                self.db.init_app(self.app)
                # create all tables
                self.db.create_all()
            except Exception as e:
                print("got the following exception when attempting db.create_all() in __init__.py: " + str(e))
            finally:
                print("db.create_all() in __init__.py was successfull - no exceptions were raised")

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginate_questions(self):
        """Test_____________"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000", json={"Art": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()