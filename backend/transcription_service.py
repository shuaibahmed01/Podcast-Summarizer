from openai import OpenAI
from dotenv import load_dotenv
import os

class TranscriptionService:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("No OpenAI API key found in environment variables")
        self.client = OpenAI(api_key=self.openai_api_key)
        

    def transcribe(self, file_path):
        audio_file = open(file_path, "rb")
        response = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return response.text



    def transcribe_and_diarize(self, file_path):
        print('0')
        transcript = self.transcribe(file_path)
        print('1')
        # diarization = self.diarize(file_path)
        print('2')
        return transcript
