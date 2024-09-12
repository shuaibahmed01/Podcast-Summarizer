import os
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import tempfile

class ChunkedTranscriptionService:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("No OpenAI API key found in environment variables")
        self.client = OpenAI(api_key=self.openai_api_key)
        self.chunk_size = 25 * 1024 * 1024  # 25 MB in bytes

    def transcribe_chunk(self, chunk_file):
        with open(chunk_file, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return response.text

    def split_audio(self, file_path):
        audio = AudioSegment.from_file(file_path)
        duration = len(audio)
        chunk_duration = int((self.chunk_size / os.path.getsize(file_path)) * duration)
        
        chunks = []
        for i in range(0, duration, chunk_duration):
            print(i)
            chunk = audio[i:i+chunk_duration]
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                chunk.export(temp_file.name, format="mp3")
                chunks.append(temp_file.name)
        
        return chunks

    def transcribe_and_diarize(self, file_path):
        chunks = self.split_audio(file_path)
        transcripts = []

        for chunk in chunks:
            transcript = self.transcribe_chunk(chunk)
            transcripts.append(transcript)
            os.unlink(chunk)  # Delete the temporary chunk file

        full_transcript = " ".join(transcripts)
        return full_transcript
