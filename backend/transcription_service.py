import openai

class TranscriptionService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def transcribe(self, file_path):
        with open(file_path, 'rb') as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
        return response['text']