# instantiate the pipeline
from pyannote.audio import Pipeline
from huggingface_hub import login
from pyannote.audio.pipelines.utils.hook import ProgressHook


# Add this line before creating the pipeline
login(token="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")
pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token="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")
print('here')

with ProgressHook() as hook:
    diarization = pipeline("/Users/shuaibahmed/Downloads/hamza-yusuf-muslimcentral.com-these-are-precious-days-2023-04-15.mp3", hook=hook)
print('1')
# dump the diarization output to disk using RTTM format
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)