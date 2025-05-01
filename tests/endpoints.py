import unittest
from app import app  # Import your Flask app

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Create a test client
        cls.app.testing = True  # Enable testing mode

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response is OK

if __name__ == '__main__':
    unittest.main()