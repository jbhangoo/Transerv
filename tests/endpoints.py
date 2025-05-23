import os
import sys
sys.path.append( os.path.join( os.path.dirname(__file__), ".."))
import pytest
import unittest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing
    with app.test_client() as client:
        yield client

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Create a test client
        cls.app.testing = True  # Enable testing mode
        cls.app.debug = True
        cls.app.csrf_enabled = False

    def test_dashboard(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response is OK

    def test_project_report(self):

        app.config['WTF_CSRF_ENABLED'] = False  # Set CSRF disabled on the app
        self.app = app.test_client()  # Recreate the test client with updated config
        self.app.testing = True

        # Test display of the form
        response = self.app.get('/reports/project', follow_redirects=True)


        response = self.app.post('/reports/project', data={'project': '1'})
        self.assertEqual(response.status_code, 200, response.data)  # Check if the response is OK

if __name__ == '__main__':
    unittest.main()
