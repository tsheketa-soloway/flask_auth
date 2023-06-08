import os
import unittest
import tempfile
from flask import jsonify
from app import app, db
from models import User
from services import create_user, get_all_users, get_user, update_user, delete_user

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_create_user(self):
        user = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com"
        }
        response = self.app.post('/api/users', json=user)
        self.assertEqual(response.status_code, 201)
        data = jsonify(response.get_json())
        self.assertEqual(data['username'], user['username'])
        self.assertEqual(data['email'], user['email'])

    def test_get_all_users(self):
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        user = User(username="testuser", password="testpassword", email="testuser@example.com")
        db.session.add(user)
        db.session.commit()
        response = self.app.get(f'/api/users/{user.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        user = User(username="testuser", password="testpassword", email="testuser@example.com")
        db.session.add(user)
        db.session.commit()
        update = {
            "username": "updateduser"
        }
        response = self.app.put(f'/api/users/{user.id}', json=update)
        self.assertEqual(response.status_code, 200)
        data = jsonify(response.get_json())
        self.assertEqual(data['username'], update['username'])

    def test_delete_user(self):
        user = User(username="testuser", password="testpassword", email="testuser@example.com")
        db.session.add(user)
        db.session.commit()
        response = self.app.delete(f'/api/users/{user.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
