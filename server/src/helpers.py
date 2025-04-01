import ffmpeg
import whisper
import numpy as np

from fastapi import UploadFile

from src.database import Query

def download(model_name: str, db):
    """
    Download a Whisper ASR model.
    """
    db.insert({"name": model_name, "downloaded": False})
    whisper.load_model(model_name)
    db.update({"downloaded": True}, Query().name == model_name)

def get_zoom_raw_audio_options()-> dict:
    return {
        "ac": 1,
        "ar": 32000,
        "format": "s16le"
    }

# Modified
# https://github.com/openai/whisper/blob/main/whisper/audio.py
def load_audio(file: UploadFile, sr: int = 16000, is_zoom_audio: bool = False):
    """
    Open an audio file object and read as mono waveform, resampling as necessary.
    """
    try:
        print(sr)
        out, _ = (
            ffmpeg.input("pipe:", threads=0, **(get_zoom_raw_audio_options() if is_zoom_audio else {}))
            .output("-", format="s16le", ar=sr, ac=1, acodec="pcm_s16le")
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True, input=file.file.read())
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
