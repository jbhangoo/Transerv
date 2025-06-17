""" Tests that actually invoke the endpoints """
import unittest
import os
import sys
from app import app
sys.path.append( os.path.join( os.path.dirname(__file__), ".."))

class BasicTests(unittest.TestCase):
    """ Test the endpoints """

    @classmethod
    def setUpClass(cls):
        """ Sets up the test client to invoke the endpoints """
        cls.app = app.test_client()  # Create a test client

    def test_dashboard(self):
        """ Basic test of the main page """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response is OK

    def test_project_report(self):
        """ Test the project report endpoint """
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF to test the endpoint

        response = self.app.get('/reports/project')
        self.assertEqual(response.status_code, 200, response.data)  # Check if the response is OK

        response = self.app.post('/reports/project')
        self.assertEqual(response.status_code, 200, response.data)  # Check if the response is OK

        response = self.app.post('/reports/project', data={'project': '1'})
        self.assertEqual(response.status_code, 200, response.data)  # Check if the response is OK

if __name__ == '__main__':
    unittest.main()
