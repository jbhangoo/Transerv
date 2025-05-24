import os
import sys
sys.path.append( os.path.join( os.path.dirname(__file__), ".."))
import unittest
from app import app

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Create a test client

    def test_dashboard(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response is OK

    def test_project_report(self):
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF to test the endpoint

        response = self.app.get('/reports/project')
        self.assertEqual(response.status_code, 200, response.data)  # Check if the response is OK

        response = self.app.post('/reports/project')
        self.assertEqual(response.status_code, 200, response.data)  # Check if the response is OK

        response = self.app.post('/reports/project', data={'project': '1'})
        self.assertEqual(response.status_code, 200, response.data)  # Check if the response is OK

if __name__ == '__main__':
    unittest.main()
