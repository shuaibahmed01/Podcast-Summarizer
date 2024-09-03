from openai import OpenAI
from dotenv import load_dotenv
import os
from pyannote.audio import Pipeline
import torch
class TranscriptionService:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.hf_token = os.getenv('HUGGING_FACE_TOKEN')
        if not self.openai_api_key:
            raise ValueError("No OpenAI API key found in environment variables")
        if not self.hf_token:
            raise ValueError("No Hugging Face token found in environment variables")
        self.client = OpenAI(api_key=self.openai_api_key)
        print('0')
        self.diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                                             use_auth_token=self.hf_token)
        print('0.5')

    def transcribe(self, file_path):
        audio_file = open(file_path, "rb")
        response = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return response.text

    def diarize(self, file_path):
        diarization = self.diarization_pipeline(file_path)
        return diarization

    def transcribe_and_diarize(self, file_path):
        transcript = self.transcribe(file_path)
        print('1')
        diarization = self.diarize(file_path)
        print('2')
        # Combine transcription and diarization
        diarized_transcript = []
        print('3')
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segment = {
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker,
                "text": transcript[int(turn.start * 100):int(turn.end * 100)]
            }
            diarized_transcript.append(segment)
        print('4')
        
        return diarized_transcript