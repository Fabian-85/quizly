from pathlib import Path
import whisper


def transcribe_audio(file_path):

    try:
        path = Path(file_path)
        model = whisper.load_model("turbo")
        result = model.transcribe(str(path))
        return result["text"]
    
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")
