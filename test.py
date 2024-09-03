# instantiate the pipeline
from pyannote.audio import Pipeline
from huggingface_hub import login
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment

# Load the audio file
audio = AudioSegment.from_file("/Users/shuaibahmed/Downloads/hamza-yusuf-muslimcentral.com-these-are-precious-days-2023-04-15.mp3")

# Optionally, you can convert it to a different format or set a specific sample rate
audio = audio.set_frame_rate(16000)  # Set sample rate if needed

# Export the audio file
audio.export("/Users/shuaibahmed/Downloads/processed_audio.wav", format="wav")

# Add this line before creating the pipeline
login(token="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")
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token="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")
print('here')

with ProgressHook() as hook:
    diarization = pipeline("/Users/shuaibahmed/Downloads/processed_audio.wav", hook=hook)

print('1')
# dump the diarization output to disk using RTTM format
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)