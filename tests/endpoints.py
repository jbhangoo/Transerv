import os
import sys
sys.path.append( os.path.join( os.path.dirname(__file__), ".."))
import unittest
from app import app

from html.parser import HTMLParser

csrf_token = None
class CsrfHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            values = [v for k, v in attrs]
            if 'csrf-token' in values:
                print("Found csrf-token", attrs)
                for name, value in attrs:
                    if name == 'content':
                        csrf_token = value

    def handle_endtag(self, tag):
        pass #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        pass #print("Encountered some data  :", data)

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Create a test client
        cls.app.testing = True  # Enable testing mode

    def test_dashboard(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response is OK

    def test_project_report(self):
        # Test display of the form
        response = self.app.get('/reports/project', follow_redirects=True)

        # Test submission of the form
        response = self.app.post('/reports/project', data={})
        self.assertEqual(response.status_code, 400)  # Check if the response is BAD REQUEST

        response = self.app.get('/', data={})
        print("GO\n")
        import html
        bytes_data = response.data
        parser = CsrfHtmlParser()
        parser.feed(bytes_data.decode('utf-8'))
        print(csrf_token)
        print(csrf_token)
        print(csrf_token)
        html_output = html.escape(bytes_data.decode('utf-8'))

        response = self.app.post('/reports/project', data={'project': '1'})
        self.assertEqual(response.status_code, 200)  # Check if the response is OK

if __name__ == '__main__':
    unittest.main()
