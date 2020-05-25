import json
from unittest.mock import patch

from django.test import TestCase


class ConvertViewTestCase(TestCase):
    @patch(
        'urllib.request.urlopen',
        return_value=open(
            'currency_converter/tests/unit/eurofxref-hist-90d.xml', 'r'))
    def test_default_parameters(self, mock_urlopen):
        """
        Convert should return converted amount with default parameters
        """
        response = self.client.get('/convert/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'amount': 0.0, 'currency': 'EUR'},
            )

        response = self.client.get('/convert/?&amount=20.0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'amount': 20.00, 'currency': 'EUR'},
            )

        response = self.client.get('/convert/?amount=20.0&reference_date=2020-05-20&src_currency=USD')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'amount': 18.25, 'currency': 'EUR'},
            )

        response = self.client.get('/convert/?amount=20.0&reference_date=2020-05-20&dest_currency=USD')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'amount': 21.92, 'currency': 'USD'},
            )

    @patch(
        'urllib.request.urlopen',
        return_value=open(
            'currency_converter/tests/unit/eurofxref-hist-90d.xml', 'r'))
    def test_invalid_input(self, mock_urlopen):
        """
        Convert should raise 404 on POST request or invalid request
        """
        response = self.client.post('/convert/?amount=20.0&date=2020-05-20')
        self.assertEqual(response.status_code, 404)
