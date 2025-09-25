from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RefreshTokenTests(APITestCase):

    old_access_token =''

    def setUp(self):
        self.user = User.objects.create_user(username='Fabian', email='fabian@mail.de', password='11111111')
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'Fabian',
            'password': '11111111'
        })
        self.old_access_token = response.cookies["access_token"]

    def test_refresh_access_token(self):
        url = reverse('refresh_token')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.old_access_token, response.cookies["access_token"])
        self.assertIn("access_token", response.cookies)



class RefreshTokenFailedTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Fabian', email='fabian@mail.de', password='11111111')
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'Fabian',
            'password': '11111111'
        })
        response.cookies["refresh_token"] ='11111'

    def test_refresh_failed_access_token(self):
        url = reverse('refresh_token')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access_token", response.cookies)
   
   