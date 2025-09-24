from pathlib import Path
import whisper

def transcribe_audio(file_path):
    path = Path(file_path)
    model = whisper.load_model("turbo")
    result = model.transcribe(str(path))
    return result["text"]