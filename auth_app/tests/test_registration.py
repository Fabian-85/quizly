from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Fabian', email='fabian@mail.de', password='11111111')

    def test_create_new_user(self):
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'testuser',
            'email': 'test_user@mail.de',
            'password': 'testuser123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_existing_username(self):
        url = reverse('register')

        response = self.client.post(url, {
            'username': 'Fabian',
            'email': 'test_user@mail.de',
            'password': 'testuser123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_existing_email(self):
        url = reverse('register')

        response = self.client.post(url, {
            'username': 'testuser',
            'email': 'fabian@mail.de',
            'password': 'testuser123'
        })
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
