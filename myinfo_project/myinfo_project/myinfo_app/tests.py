from rest_framework.test import APITestCase
from django.urls import reverse

class MyInfoTests(APITestCase):
    def test_auth_url(self):
        """
        Test the generation of the MyInfo authorization URL.
        """
        response = self.client.get(reverse('auth-url'))
        self.assertEqual(response.status_code, 200)  # Status should be 200 OK
        self.assertIn('auth_url', response.data)  # Response should contain 'auth_url'
        self.assertIn('code_verifier', response.data)  # Response should contain 'code_verifier'

    def test_access_token_missing_params(self):
        """
        Test the access token retrieval when parameters are missing.
        """
        response = self.client.post(reverse('access-token'), data={})
        self.assertEqual(response.status_code, 400)  # Status should be 400 Bad Request
        self.assertIn('auth_code', response.data)  # Missing 'auth_code' should trigger validation error
        self.assertIn('oauth_state', response.data)  # Missing 'oauth_state' should trigger validation error
        self.assertIn('code_verifier', response.data)  # Missing 'code_verifier' should trigger validation error

    def test_retrieve_data_missing_access_token(self):
        """
        Test user data retrieval when access token is missing.
        """
        response = self.client.post(reverse('retrieve-data'), data={})
        self.assertEqual(response.status_code, 400)  # Status should be 400 Bad Request
        self.assertIn('access_token', response.data)  # Missing 'access_token' should trigger validation error
