import os

from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribeAudio(audioBytes: bytes, language: Optional[str] = None) -> dict:
    try:
        audioFile = ("audio.mp3", audioBytes, "audio/mpeg")
        
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audioFile,
            language=language,
            response_format = "json"
        )
        return {
            "text": response.text,
            "language": language or "auto-detected"

        }
        
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")