from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from quiz_app.models import Quiz, Question


class GetSingleQuizTests(APITestCase):


    def setUp(self):
        self.user1 = User.objects.create_user(username='Fabian', email='fabian@mail.de', password='11111111')
        self.user2 = User.objects.create_user(username='test_user', email='test@mail.de', password='11111111')
        self.quiz = Quiz.objects.create(user=self.user1,title="Quiz Title",description="Quiz Description",video_url="https://www.youtube.com/watch?v=example")
        self.question1 = Question.objects.create(quiz=self.quiz,question_title="Question 1",question_options=["Option A", "Option B", "Option C", "Option D"],answer="Option A")
        self.question2 = Question.objects.create(quiz=self.quiz,question_title="Question 2",question_options=["Option A", "Option B", "Option C", "Option D"],answer="Option C")
        self.question3 = Question.objects.create(quiz=self.quiz,question_title="Question 3",question_options=["Option A", "Option B", "Option C", "Option D"],answer="Option B")
        self.url=reverse('single-quiz', kwargs={'pk':self.quiz.id})
        self.quiz_count = Quiz.objects.all().count()
    
    def test_delete_quiz_authenticated_owner_returns_200(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.url)
        new_quiz_count = Quiz.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.quiz_count-1, new_quiz_count)

    def test_delete_quiz_with_wrong_user_returns_401(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.url)
        new_quiz_count = Quiz.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.quiz_count, new_quiz_count)

    def test_delete_quiz_unauthenticated_returns_401(self):
        response = self.client.delete(self.url)
        new_quiz_count = Quiz.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.quiz_count, new_quiz_count)

    def test_delte_quiz_dont_exist_and_user_unauthenticated_returns_404(self):
        url=reverse('single-quiz', kwargs={'pk':9999})
        response = self.client.delete(url)
        new_quiz_count = Quiz.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.quiz_count, new_quiz_count)

    def test_delete_quiz_dont_exist_returns_401(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        url=reverse('single-quiz', kwargs={'pk':9999})
        response = self.client.delete(url)
        new_quiz_count = Quiz.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.quiz_count, new_quiz_count)
