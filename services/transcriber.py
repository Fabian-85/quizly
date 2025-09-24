from pathlib import Path
import whisper


def transcribe_audio(file_path):

    """
    Transcribe audio file to text using Whisper AI.
    
    - file_path: Path to the audio file to be transcribed.
    - Returns: Transcribed text.
    """

    try:
        path = Path(file_path)
        model = whisper.load_model("turbo")
        result = model.transcribe(str(path))
        return result["text"]
    
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")
