from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quiz_app.models import Quiz
from quiz_app.api.serializers import QuizSerializer, SingleQuizSerializer
from quiz_app.api.permissions import IsOwner
from services import quiz_service
 
class CreateQuizView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):
        
        URL = request.data.get('url',None)
        if not URL:
            return Response({"error":"URL is required"}, status=400)

        try:
            quiz = quiz_service.create_quiz_from_video_url(URL)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        serializer = QuizSerializer(data=quiz, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
        

class GetAllQuizzesView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)
    
class SingleQuizView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated,IsOwner]
    queryset = Quiz.objects.all()
    serializer_class = SingleQuizSerializer

    
 

 