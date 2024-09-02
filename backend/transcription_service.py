from openai import OpenAI
from dotenv import load_dotenv
import os
class TranscriptionService:
    def __init__(self, api_key):
        load_dotenv()  # This loads the variables from .env
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("No OpenAI API key found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, file_path):
        print('here')
        audio_file = open(file_path, "rb")
        client = OpenAI()
        print("2.1")
        response = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
        print("2.2")
        return response.text