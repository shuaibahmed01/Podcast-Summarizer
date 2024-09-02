from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate
from transcription_service import TranscriptionService
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = ChatOpenAI(temperature=0.7)

template = """
You are an AI assistant that creates structured reports/summaries of podcasts. 
A user should completely understand what the podcast was about and any important information from the report you generate.

Given the following podcast transcript, please provide a comprehensive summary including:
1. Title of the podcast (if discernible)
2. Main topic
3. Key points (bullet points)
4. Interesting facts or insights
5. Conclusion or takeaways

Podcast transcript:
{transcript}

Please structure your response in a clear, easy-to-read format.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=['transcript']
)

def get_session_history():
    return ConversationBufferMemory(memory_key="history", input_key="transcript")

chain = LLMChain(
    llm=model,
    prompt=prompt,
    memory=get_session_history(),
    verbose=True
)

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        email = request.form.get('email')
        print(audio_file.filename)
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if audio_file:
            filename = audio_file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(filepath)

            # 1. Transcribe the audio file
            transcription_service = TranscriptionService(os.getenv('OPENAI_API_KEY'))

            transcript = transcription_service.transcribe(filepath)

            print(transcript)

            # 2. Generate a summary using the Langchain agent
            response = chain.run(transcript=transcript)
            print('4')
            # 3. Send the summary back to the client
            summary = {'content': response}

            # 4. Clean up the uploaded file
            os.remove(filepath)

            return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)