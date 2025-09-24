from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):

    """
    Model representing a Quiz created by a user.

    Attributes:
        title (str): The title of the quiz.
        description (str): A brief description of the quiz.
        video_url (str): The URL of the video from which the quiz is generated.
        created_at (datetime): The timestamp when the quiz was created.
        updated_at (datetime): The timestamp when the quiz was last updated.
        user (ForeignKey): The user who created the quiz.
    """

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    

    def __str__(self):
        return self.title
    
class Question(models.Model):

    """
    Model representing a Question associated with a Quiz.

    Attributes:
        quiz (ForeignKey): The quiz to which the question belongs.
        question_title (str): The text of the question.
        question_options (JSONField): A list of possible answer options.
        answer (str): The correct answer to the question.
    """
    
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_title = models.CharField(max_length=255)
    question_options = models.JSONField()   
    answer = models.CharField(max_length=255)  
    
    def __str__(self):
        return self.question_title