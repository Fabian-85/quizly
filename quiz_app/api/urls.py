from django.urls import path
from .views import CreateQuizView, GetAllQuizzesView, SingleQuizView


urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name='create_quiz'),
    path('quizzes/', GetAllQuizzesView.as_view(), name='create_quiz'),
    path('quizzes/<int:pk>/', SingleQuizView.as_view(), name='create_quiz'),
]
