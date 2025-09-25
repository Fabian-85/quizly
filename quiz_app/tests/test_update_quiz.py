from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from quiz_app.models import Quiz, Question


quiz={
  "title": "Quiz Title 2",
  "description": "Quiz Description",
  "created_at": "2023-07-29T12:34:56.789Z",
  "updated_at": "2023-07-29T12:34:56.789Z",
  "video_url": "https://www.youtube.com/watch?v=svddes",
  "questions": [
    {
      "question_title": "Question 1",
      "question_options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option A"
    }
  ]
}


class GetSingleQuizTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='Fabian', email='fabian@mail.de', password='11111111')
        self.user2 = User.objects.create_user(username='test_user', email='test@mail.de', password='11111111')
        self.quiz = Quiz.objects.create(user=self.user1,title="Quiz Title",description="Quiz Description",video_url="https://www.youtube.com/watch?v=example")
        self.question1 = Question.objects.create(quiz=self.quiz,question_title="Question 1",question_options=["Option A", "Option B", "Option C", "Option D"],answer="Option A")
        self.question2 = Question.objects.create(quiz=self.quiz,question_title="Question 2",question_options=["Option A", "Option B", "Option C", "Option D"],answer="Option C")
        self.question3 = Question.objects.create(quiz=self.quiz,question_title="Question 3",question_options=["Option A", "Option B", "Option C", "Option D"],answer="Option B")
        self.url=reverse('single-quiz', kwargs={'pk':self.quiz.id})
    
    def test_partial_update_quiz_authenticated_user_returns_200(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.url,{"title": "Update"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Update")

    def test_full_update_quiz_authenticated_user_returns_200(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.url,{"title": "Update","description":"description"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Update")
        self.assertEqual(response.data["description"], "description")

    def test_full_update_check_that_only_description_and_title_can_updated_returns_200(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        response_data_before_update = self.client.get(self.url)
        response = self.client.patch(self.url,quiz)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Quiz Title 2")
        self.assertEqual(response.data["description"], "Quiz Description")
        self.assertEqual(response.data["video_url"],"https://www.youtube.com/watch?v=example")
        self.assertEqual(response.data["questions"], response_data_before_update.data["questions"])

    def test_patch_quiz_with_wrong_user_returns_403(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.url,{"title": "Update"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_quiz_unauthenticated_returns_401(self):
        response = self.client.patch(self.url,{"title": "Update"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_quiz_dont_exist_and_user_unauthenticated_returns_401(self):
        url=reverse('single-quiz', kwargs={'pk':9999})
        response = self.client.patch(url,{"title": "Update"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_quiz_dont_exist_returns_404(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        url=reverse('single-quiz', kwargs={'pk':9999})
        response = self.client.patch(url,{"title": "Update"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
