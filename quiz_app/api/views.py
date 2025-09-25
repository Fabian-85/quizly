from rest_framework import generics,mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quiz_app.models import Quiz
from quiz_app.api.serializers import CreateQuizSerializer, QuizSerializer
from quiz_app.api.permissions import IsOwner
from services import quiz_service
 
class CreateQuizView(APIView):

    """View to create a quiz from a video URL.
    
        -POST:
            - condition: youtube url is required in the request body.

            Workflow:
                1. Downloads the audio from the provided youtube URL with yt-dlp.
                2. Transcribes the audio to text with whisperAi.
                3. Generates a quiz with 10 questions from the transcribed text with gemini.

            - Returns: The created quiz data.
            - Permissions: Only authenticated users can access.
    """

    permission_classes = [IsAuthenticated]


    def post(self, request):
        
        URL = request.data.get('url',None)
        if not URL:
            return Response({"error":"URL is required"}, status=400)

        try:
            quiz = quiz_service.create_quiz_from_video_url(URL)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        serializer = CreateQuizSerializer(data=quiz, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
        

class GetAllQuizzesView(generics.ListAPIView):

    """
    View to get all quizzes created by the authenticated user.
    
    - GET:
        - Returns: A list of quizzes created by the authenticated user.
        - Permissions: Only authenticated users can access.
    """

    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)
    
class SingleQuizView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):

    """
    View to retrieve, update, or delete a single quiz by its ID.

    - GET:
        - Returns: The quiz data for the specified ID.
        - Permissions: Only the owner of the quiz can access.

    - PATCH:
        - Updates: The quiz data for the specified ID.
        - Only the fields 'title' and 'description' can be updated.
        - Permissions: Only the owner of the quiz can update.

    - DELETE:
        - Deletes: The quiz for the specified ID.
        - Permissions: Only the owner of the quiz can delete.
    """

    permission_classes = [IsAuthenticated,IsOwner]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    
 

 