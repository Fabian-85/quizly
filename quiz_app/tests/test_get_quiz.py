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
    
    def test_get_quiz_authenticated_owner_returns_200(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data

        for key in ("id", "title", "description", "created_at", "updated_at", "video_url", "questions"):
            self.assertIn(key, data)
        self.assertEqual(len(data["questions"]), 3)
        for key in ("id", "question_title", "question_options", "answer"):
            self.assertIn(key,  data["questions"][0])
        for question in data["questions"]:
            self.assertEqual(len(question["question_options"]), 4)
            self.assertIn(question["answer"], question["question_options"])


    def test_get_quiz_with_wrong_user_returns_403(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_quiz_unauthenticated_returns_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_quiz_dont_exist_and_user_unauthenticated_returns_401(self):
        url=reverse('single-quiz', kwargs={'pk':9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_quiz_dont_exist_returns_404(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        url=reverse('single-quiz', kwargs={'pk':9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




    

    
   

