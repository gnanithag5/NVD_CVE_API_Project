# unit_tests.py

import unittest
from app2 import app  # Importing the Flask app from app2.py
from flask import Flask
from flask.testing import FlaskClient

class FlaskTestCase(unittest.TestCase):

    # Setup test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True  # Enable test mode

    # Test if the /cves/list route loads successfully
    def test_cve_list(self):
        response = self.app.get('/cves/list')
        self.assertEqual(response.status_code, 200)  # Should return HTTP 200
        self.assertIn(b'CVE List', response.data)  # Check if "CVE List" is in the response

    # Test if pagination works
    def test_cve_list_pagination(self):
        response = self.app.get('/cves/list?page=2&resultsPerPage=10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CVE List', response.data)

    # Test if a specific CVE ID detail page loads correctly
    def test_cve_detail(self):
        response = self.app.get('/cves/CVE-1999-0095')  # Use an existing CVE ID
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CVE Details', response.data)

    # Test for a non-existent CVE ID
    def test_cve_not_found(self):
        response = self.app.get('/cves/CVE-9999-0000')  # Use a non-existent CVE ID
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'CVE ID not found', response.data)

    # Test if results per page selection works
    def test_results_per_page(self):
        response = self.app.get('/cves/list?resultsPerPage=50')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()