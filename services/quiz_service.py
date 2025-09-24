import os
from services import downloader, transcriber, gemini_quiz_service


def create_quiz_from_video_url(url):
    VIDEO_PATH = downloader.download_audio_from_youtube(url)
    video_transcript = transcriber.transcribe_audio(VIDEO_PATH)
    quiz = gemini_quiz_service.gerate_quiz_from(video_transcript)
    quiz['video_url'] = url
    os.remove(VIDEO_PATH)
    return quiz