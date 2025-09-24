from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services import downloader, transcriber, gemini_quiz_service
from quiz_app.api.serializers import QuizSerializer

video_transcript = """
Gibt so Sachen die hasst echt jeder. Kein Schnee im Winter. Bäh. Regen im Sommer. Alter. Aber wisst ihr was am schlimmsten ist? Mathe in der Schule. Egal wann. Warum? Weil es da so Worte gibt wie Sinus, Cosinus und Tangens. Aber wir klären euch mal auf. Angefangen hat alles mit nem Kreis. Aber nicht irgendein Kreis, sondern der Einheitskreis. Also ein Kreis mit Radius 1. Da hat jetzt irgendein Schlaumeier mal ein Koordinatenkreuz durchgelegt. Wow. Dann hat jemand gemerkt, ey ich messe mal die x und die y Koordinate von dem Punkt hier. Und das je nachdem wie groß der Winkel in der Mitte ist. Die hellblaue Linie ist y. Die grüne x. Wenn man den Winkel nämlich größer macht, kriegt man auch andere x und y Koordinaten raus. Hier ist y größer, x aber kleiner als vorhin. Wenn man den Winkel noch größer macht, gibt es sogar negative Koordinaten. Man kann jetzt die y Koordinate in ein Diagramm machen. Je nachdem wie groß der Winkel ist, ändert sich ja das y. Sieht dann so aus. Vielleicht habt ihr es ja schon mal gesehen. Genau. Das ist der Sinus. Man sagt dann, die y Koordinate von dem Punkt ist der Sinus von Alpha. Wenn man stattdessen die x Koordinate aufmalt über dem Winkel sieht es so aus. Könnt ihr euch auch bekannt vorkommen. Das ist der Cosinus. Gleiches Spiel. Der Cosinus von Alpha ist x. Und einen gibt es noch. Wenn man die y Koordinate durch die x Koordinate teilt, dann sieht es nämlich so aus. Ganz schön hässlich, wa? Was wird dieses wohl sein? Klar, steht ja im Video Titel. Der Tangens. Hier sagt man, der Tangens von Alpha ist y durch x. Aber was bringt uns das jetzt? Schauen wir uns dazu mal ein Dreieck an. Nur ohne Kreis drum. Die hellblaue Linie heißt jetzt aber nimmer y Koordinate, sondern Gegenkathete, weil sie gegenüber vom Winkel ist. Die grüne Linie heißt auch nimmer x Koordinate, die heißt Ankathete, weil sie AN dem Winkel dran liegt. Und die graue ist bei normalen Dreiecken ja auch nicht einfach nur 1 lang. Die kriegt deswegen auch nen Namen. Hypotenuse. Kotz, was für ein Wort. Wenn das graue Ding nur 1 lang ist, gehts wie vorhin. Nur jetzt mit dem neuen Namen. Die Gegenkathete ist der Sinus von Alpha. Vorhin war ja y gleich Sinus von Alpha. Wenn jetzt ja aber das graue Ding länger ist, werden ja auch die beiden blauen Striche länger. Sagen wir mal, das graue ist 3 mal so lang. Dann sind auch die Gegenkathete und die Ankathete 3 mal so lang. Also ist die gesamte Gegenkathete der Sinus von Alpha mal 3. Und die Hypotenuse ist ja gerade 3. Also ist die Gegenkathete gleich Sinus von Alpha mal Hypotenuse. Das kann man jetzt noch umformen. Dann hat man die Form wie ihr sie euch merken müsst. Sinus ist Gegenkathete durch Hypotenuse. Zur Erinnerung, wegen dem blöden Namen. Das lange ist die Hypotenuse. Am Winkel dran die Ankathete, gegenüber die Gegenkathete. Also wir merken uns. 1. Sinus. Der Sinus von Alpha gleich Gegenkathete durch Hypotenuse. Dann natürlich der 2. Kosinus. Der Kosinus von Alpha gleich Ankathete durch Hypotenuse. Und zuletzt der 3. Tangens. Der Tangens von Alpha gleich Gegenkathete durch Ankathete. Aber wichtig, nur bei rechtwinkligen Dreiecken. Apropos rechtwinklige Dreiecke. Klickt hier rechts und erfahrt mehr über den Satz des Pythagoras. So Leute ihr habt gerade 3 der meistgehassten Worte in Mathematik durchgebracht und ihr lebt noch. Das ist doch ein Grund zu feiern. Würde ich am liebsten Hashtag nackt durch die Fußgängertone tanzen oder doch Hashtag erstmal einen Tag durchbennen. Teilt es uns mit und allen anderen. Liked und teilt und vergesst nicht auch in Zukunft wieder vorbeizuschauen. Wir haben euch lieb. Also bis dann und ciao.
"""
quiz = {
    "title": "Sinus, Cosinus, Tangens: A Quick Quiz",
    "description": "This quiz covers the fundamental concepts of Sinus, Cosinus, and Tangens, starting from the unit circle definition to their application in right-angled triangles.",
    "questions": [
        {
            "question_title": "What is the defining characteristic of a unit circle?",
            "question_options": [
                "Radius 0",
                "Radius 1",
                "Radius 2",
                "Radius variable"
            ],
            "answer": "Radius 1"
        },
        {
            "question_title": "In the context of the unit circle, which coordinate represents the Sinus of an angle (Alpha)?",
            "question_options": [
                "x-coordinate",
                "y-coordinate",
                "z-coordinate",
                "origin coordinate"
            ],
            "answer": "y-coordinate"
        },
        {
            "question_title": "In the context of the unit circle, which coordinate represents the Cosinus of an angle (Alpha)?",
            "question_options": [
                "x-coordinate",
                "y-coordinate",
                "z-coordinate",
                "origin coordinate"
            ],
            "answer": "x-coordinate"
        },
        {
            "question_title": "How is the Tangent function defined using the x and y coordinates from the unit circle?",
            "question_options": [
                "x divided by y",
                "y multiplied by x",
                "y divided by x",
                "x minus y"
            ],
            "answer": "y divided by x"
        },
        {
            "question_title": "In a right-angled triangle, what is the name for the side located directly opposite the angle (Alpha)?",
            "question_options": [
                "Ankathete",
                "Hypotenuse",
                "Gegenkathete",
                "Nebenkathete"
            ],
            "answer": "Gegenkathete"
        },
        {
            "question_title": "In a right-angled triangle, what is the name for the side located adjacent to the angle (Alpha)?",
            "question_options": [
                "Gegenkathete",
                "Hypotenuse",
                "Ankathete",
                "Diagonale"
            ],
            "answer": "Ankathete"
        },
        {
            "question_title": "What is the name of the longest side in a right-angled triangle?",
            "question_options": [
                "Ankathete",
                "Gegenkathete",
                "Hypotenuse",
                "Schenkel"
            ],
            "answer": "Hypotenuse"
        },
        {
            "question_title": "What is the correct formula for calculating the Sinus of an angle (Alpha) in a right-angled triangle?",
            "question_options": [
                "Ankathete / Hypotenuse",
                "Gegenkathete / Ankathete",
                "Gegenkathete / Hypotenuse",
                "Hypotenuse / Gegenkathete"
            ],
            "answer": "Gegenkathete / Hypotenuse"
        },
        {
            "question_title": "What is the correct formula for calculating the Cosinus of an angle (Alpha) in a right-angled triangle?",
            "question_options": [
                "Gegenkathete / Hypotenuse",
                "Ankathete / Gegenkathete",
                "Ankathete / Hypotenuse",
                "Hypotenuse / Ankathete"
            ],
            "answer": "Ankathete / Hypotenuse"
        },
        {
            "question_title": "What is the correct formula for calculating the Tangens of an angle (Alpha) in a right-angled triangle?",
            "question_options": [
                "Ankathete / Hypotenuse",
                "Gegenkathete / Ankathete",
                "Hypotenuse / Ankathete",
                "Gegenkathete / Hypotenuse"
            ],
            "answer": "Gegenkathete / Ankathete"
        }
    ],
    "video_url": "https://www.youtube.com/watch?v=AWZW1OwpT-w"
}

class CreateQuizView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):
        #URL = request.data.get('url')
        #VIDEO_PATH = downloader.download_audio_from_youtube(URL)
        #video_transcript = transcriber.transcribe_audio(VIDEO_PATH)
        #quiz = gemini_quiz_service.gerate_quiz_from(video_transcript)
        #quiz['video_url'] = URL

         
        serializer = QuizSerializer(data=quiz, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
 

 