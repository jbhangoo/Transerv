import os
import sys
sys.path.append( os.path.join( os.path.dirname(__file__), ".."))
import unittest
from routes.ajax import url_get
class UtilsTests(unittest.TestCase):

    def test_get_url(self):
        # Example usage with a valid JSON API endpoint.
        lat, lon, wdate = 51.5074, -0.1278, "2023-06-01"
        valid_url = "https://jsonplaceholder.typicode.com/todos/1"  # A reliable test URL
        invalid_url = "https://nonexistent-domain.example"
        non_json_url = "https://www.google.com"  # URL that returns HTML, not JSON

        url_get(valid_url, True)
        url_get(invalid_url, False)
        url_get(non_json_url, False)
