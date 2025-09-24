from rest_framework import serializers
from quiz_app.models import Quiz, Question



class QuestionSerializer(serializers.ModelSerializer):

    """
    Serializer for Question model with validation for question options and answer.

    Methods:
        - validate_question_options: Ensures exactly 4 distinct options.
        - validate: Ensures the answer is one of the options.
    """

    question_options = serializers.ListField(
        child=serializers.CharField(max_length=255, allow_blank=False),
        min_length=4, max_length=4
    )

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']

    def validate_question_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("There must be exactly 4 answer options.")
        if len(set(value)) != 4:
            raise serializers.ValidationError("Answer options must be distinct.")
        return value
    
    def validate(self, attrs):
        options = attrs.get('question_options')
        answer = attrs.get('answer')
        if answer not in options:
            raise serializers.ValidationError("The answer must be one of the question options.")
        return attrs


class CreateQuizSerializer(serializers.ModelSerializer):

    """
    Serializer for creating a Quiz with nested questions.

    Method:
        - create: Handles creation of Quiz and associated Questions.
    """

    questions = QuestionSerializer(many=True)
    

    class Meta:
        model = Quiz
        fields =['id', 'title', 'description', 'created_at', 'updated_at','video_url', 'questions']



    def create(self, validated_data):
        user= self.context['request'].user
        questions = validated_data.pop('questions',None)
        quiz = Quiz.objects.create(**validated_data, user=user)
        if questions:
            for question_data in questions:
                Question.objects.create(quiz=quiz, **question_data)
        return quiz
    
class QuizSerializer(serializers.ModelSerializer):

    """
    Serializer for Quiz model with nested questions (read-only) for retrieving all quizzes that user are created
    and retrieving, updatung and deleting a single offer.
    """

    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields =['id', 'title', 'description', 'created_at', 'updated_at','video_url', 'questions']
        extra_kwargs = {
            'video_url': {'read_only': True}
        }
