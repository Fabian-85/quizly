from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken


class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Fabian', email='fabian@mail.de', password='11111111')
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'Fabian',
            'password': '11111111'
        })

    def test_logout_with_correct_credentials(self):
        access = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse('logout')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_wrong_credentials(self):
        url = reverse('logout')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        