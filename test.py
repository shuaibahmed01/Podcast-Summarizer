# instantiate the pipeline
from pyannote.audio import Pipeline
from huggingface_hub import login
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment
from openai import OpenAI
# Load the audio file
audio = AudioSegment.from_file("/Users/shuaibahmed/Downloads/hamza-yusuf-muslimcentral.com-these-are-precious-days-2023-04-15.mp3")

# Optionally, you can convert it to a different format or set a specific sample rate
audio = audio.set_frame_rate(16000)  # Set sample rate if needed

# Export the audio file
audio.export("/Users/shuaibahmed/Downloads/processed_audio.wav", format="wav")
print('1')

print('2')
# Add this line before creating the pipeline
login(token="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")
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token="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")
print('here')

with ProgressHook() as hook:
    diarization = pipeline("/Users/shuaibahmed/Downloads/processed_audio.wav", hook=hook)

diarized_transcript = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
  segment_words = [
      word for word in words
      if word['start'] >= turn.start and word['end'] <= turn.end
  ]
  
  if segment_words:
      segment = {
          "start": turn.start,
          "end": turn.end,
          "speaker": speaker,
          "text": ' '.join(word['word'] for word in segment_words)
      }
      diarized_transcript.append(segment)

        
formatted_transcript = ""
for segment in diarized_transcript:
    formatted_transcript += f"\nSpeaker {segment['speaker']}: {segment['text']}"

print(formatted_transcript)