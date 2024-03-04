"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the public features of the user API."""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_crate_user_success(self):
        """Test creating a user successfully."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        
    def test_user_with_email_exists_error(self):
        """Test error return if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test name',
        }
        create_user(**payload)    
        res = self.client.post(CREATE_USER_URL, payload)          
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short_error(self):
        """Test an error return if password less than five characters."""
        payload = {
            'email': 'test@example.com',
            'password': 'pass',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
        
    def test_create_token_by_user(self):
        """Test generates token for valid credentials."""
        
        user_details = {
            'name': 'test name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)
        
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_token_bad_credentials(self):
        """Test returns error if credentials inalid."""
        create_user(email='test@example.com', password='badpass')
        
        payload = {
            'email':'test@example.com', 'password':'badpass'
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    # def test_create_token_blank_password(self):
    #     pass