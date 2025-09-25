from django.urls import path
from .views import CreateQuizView, GetAllQuizzesView, SingleQuizView


urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('quizzes/', GetAllQuizzesView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', SingleQuizView.as_view(), name='single-quiz'),
]
