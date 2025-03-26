from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

# Use Django's User model
User = get_user_model()

class UserAuthTests(APITestCase):
    
    def setUp(self):
        """Set up test data before each test."""
        # Create a test user (not superuser)
        self.user_data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.register_url = '/api/auth/users/'  # Correct Djoser register endpoint
        self.login_url = '/api/auth/token/'  # JWT login endpoint

    def test_user_registration(self):
        """Test the user registration functionality."""
        data = {
            'username': 'newuser',
            'password': 'password@123',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.register_url, data, format='json')
        
        # Debugging information for failed test cases
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Expected 201, got {response.status_code}. Response: {response.data}"
        )
        
        self.assertEqual(response.data['username'], 'newuser')
        self.assertIn('id', response.data)  # Assuming the response contains 'id'

    def test_user_login(self):
        """Test the login functionality."""
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected 200, got {response.status_code}. Response: {response.data}"
        )
        
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'username': 'wronguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            f"Expected 401, got {response.status_code}. Response: {response.data}"
        )

    def test_protected_endpoint(self):
        """Test access to a protected endpoint with JWT."""
        # Login and get token
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(
            login_response.status_code,
            status.HTTP_200_OK,
            f"Login failed. Response: {login_response.data}"
        )
        
        token = login_response.data['access']

        # Use the token to access a protected endpoint
        profile_url = '/api/auth/users/me/'  # Djoser's profile endpoint
        response = self.client.get(profile_url, HTTP_AUTHORIZATION=f'Bearer {token}')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Protected endpoint access failed. Response: {response.data}"
        )

