from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from transcription_service import ChunkedTranscriptionService
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain
from visualization_service import generate_visualizations
import threading

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = ChatOpenAI(temperature=0.7)

template = """
You are an AI assistant that creates detailed reports of lecture recordings. 
Your goal is to provide students with a thorough understanding of the lecture content, including all essential information.

Given the following lecture transcript, please provide a comprehensive report that includes:
1. Title of the lecture
2. Main topic or subject matter
3. Key points and concepts discussed
  - Include headers for each key point and elaborate on them as necessary
4. Important dates and deadlines mentioned during the lecture
5. Notable insights or quotes from the lecturer
6. Summary of any assignments or tasks given
7. Conclusion or takeaways for students
8. Overview of the lecturer and their qualifications or background if this is able to be extracted from the transcript

Feel free to add any other sections you feel a student may want and structure the sections in a way you feel makes sense

The transcript may include multiple speakers, so use context to distinguish between different individuals and their contributions. Ensure that the report is structured clearly and is easy to read for students.

lecture transcript:
{transcript}

Please structure your response in a clear, easy-to-read format using HTML tags for formatting. Use <h1> for the title, <h2> for main sections, <h3> for subsections, <p> for paragraphs, <ul> or <ol> for lists, and <blockquote> for quotes.
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

def process_audio_task(audio_file, email):
    try:
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)

        # 1. Transcribe and diarize the audio file
        transcription_service = ChunkedTranscriptionService()
        transcript = transcription_service.transcribe_and_diarize(filepath)

        # 2. Generate a summary using the Langchain agent
        response = chain.run(transcript=transcript)

        # 3. Generate visualizations using the new dynamic agent
        visualizations = generate_visualizations(transcript, response)

        # 4. Clean up the uploaded file
        os.remove(filepath)

        return {'summary': {'content': response}, 'visualizations': visualizations}
    except Exception as e:
        return {'error': str(e)}

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    email = request.form.get('email')
    
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Process the audio in the main thread
    result = process_audio_task(audio_file, email)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001, debug=True, threaded=False)