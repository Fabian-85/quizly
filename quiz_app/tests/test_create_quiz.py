from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
 


class CreateQuizTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Fabian', email='fabian@mail.de', password='11111111')
         
    def test_create_quiz(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('create-quiz')
        response = self.client.post(url, {
            'url': 'https://www.youtube.com/watch?v=SigkkLej2Bk'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_quiz_unauthenticated(self):
        url = reverse('create-quiz')
        response = self.client.post(url, {
            'url': 'testuser'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
   

