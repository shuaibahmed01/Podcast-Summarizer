from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from transcription_service import ChunkedTranscriptionService
from langchain.chains import LLMChain
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
email_password = os.getenv("EMAIL_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = ChatAnthropic(model="claude-3-5-sonnet-20240620",
                    temperature=0.7, 
                    anthropic_api_key=anthropic_api_key)

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

def send_email(receiver_email, summary):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "New Lecture Report Available!"

    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Your Lecture Summary</h1>
            {summary}
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def process_audio_task(audio_file, email):
    try:
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)

        transcription_service = ChunkedTranscriptionService()
        transcript = transcription_service.transcribe_and_diarize(filepath)

        def generate():
            yield 'data: {"progress": 50}\n\n'  # Transcription complete

            response = chain.run(transcript=transcript)

            yield 'data: {"progress": 90}\n\n'  # Summary generation complete

            # Send email
            send_email(email, response)

            yield 'data: {"progress": 100}\n\n'  # Email sent
            yield f'data: {{"summary": {json.dumps(response)}}}\n\n'

        os.remove(filepath)

        return Response(generate(), content_type='text/event-stream')
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

    return process_audio_task(audio_file, email)

if __name__ == '__main__':
    app.run(port=5001, debug=True)