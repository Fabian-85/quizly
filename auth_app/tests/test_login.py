from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class LoginTests(APITestCase):

    def setUp(self):
       
        self.user = User.objects.create_user(
            username='Fabian', email='fabian@mail.de', password='11111111')

    def test_login_with_correct_user_data(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'Fabian',
            'password': '11111111'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_login_with_wrong_password(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'Fabian',
            'password': 'testuser'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)

    def test_login_with_without_existing_user(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'Fabian123',
            'password': 'testuser'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)
