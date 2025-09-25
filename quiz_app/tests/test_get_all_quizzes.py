from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from quiz_app.models import Quiz, Question


class GetAllUserQuizzesTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='Fabian', email='fabian@mail.de', password='11111111')
        self.user2 = User.objects.create_user(
            username='test_user', email='test@mail.de', password='11111111')
        self.user3 = User.objects.create_user(
            username='user_without_quiz', email='user_without_quiz@mail.de', password='11111111')
        self.quiz1 = Quiz.objects.create(user=self.user1, title="Quiz Title",
                                         description="Quiz Description", video_url="https://www.youtube.com/watch?v=example")
        self.question1 = Question.objects.create(quiz=self.quiz1, question_title="Question 1", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option A")
        self.question2 = Question.objects.create(quiz=self.quiz1, question_title="Question 2", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option C")
        self.question3 = Question.objects.create(quiz=self.quiz1, question_title="Question 3", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option B")
        self.quiz2 = Quiz.objects.create(user=self.user1, title="Quiz Title2",
                                         description="Quiz Description2", video_url="https://www.youtube.com/watch?v=example")
        self.question1 = Question.objects.create(quiz=self.quiz2, question_title="Question 1", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option A")
        self.question2 = Question.objects.create(quiz=self.quiz2, question_title="Question 2", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option C")
        self.question3 = Question.objects.create(quiz=self.quiz2, question_title="Question 3", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option B")
        self.quiz3 = Quiz.objects.create(user=self.user2, title="Quiz Title3",
                                         description="Quiz Description3", video_url="https://www.youtube.com/watch?v=example")
        self.question1 = Question.objects.create(quiz=self.quiz3, question_title="Question 1", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option A")
        self.question2 = Question.objects.create(quiz=self.quiz3, question_title="Question 2", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option C")
        self.question3 = Question.objects.create(quiz=self.quiz3, question_title="Question 3", question_options=[
                                                 "Option A", "Option B", "Option C", "Option D"], answer="Option B")
        self.url = reverse('quiz-list')

    def test_get_all_quiz_from_user_1_returns_200(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        quizzes = response.data

        for quiz in quizzes:
            for key in ("id", "title", "description", "created_at", "updated_at", "video_url", "questions"):
                self.assertIn(key, quiz)
            for question in quiz["questions"]:
                 for key in ("id", "question_title", "question_options", "answer"):
                     self.assertIn(key, question)
                 self.assertEqual(len(question["question_options"]), 4)
                 self.assertIn(question["answer"], question["question_options"])


    def test_get_all_quiz_from_user_3_returns_200(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_quiz_unauthenticated_returns_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
