import os
from services import downloader, transcriber, gemini_quiz_service


def create_quiz_from_video_url(url):

    """
    Create a quiz from a YouTube video URL.

     Workflow:
        1. Downloads the audio from the provided youtube URL with yt-dlp.
        2. Transcribes the audio to text with whisperAi.
        3. Generates a quiz with 10 questions from the transcribed text with gemini.

    """
    
    VIDEO_PATH = downloader.download_audio_from_youtube(url)
    video_transcript = transcriber.transcribe_audio(VIDEO_PATH)
    quiz = gemini_quiz_service.gerate_quiz_from(video_transcript)
    quiz['video_url'] = url
    os.remove(VIDEO_PATH)
    return quiz