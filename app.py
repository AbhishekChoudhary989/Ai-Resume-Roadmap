import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
from google import genai
from google.genai import types
from tenacity import retry, wait_exponential_jitter, stop_after_attempt
from dotenv import load_dotenv

# --- Setup ---
load_dotenv()
# The new SDK uses a Client object
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app)

# --- Helpers ---

def extract_text_from_pdf(uploaded_file):
    """Extracts text from the uploaded PDF resume."""
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@retry(
    wait=wait_exponential_jitter(initial=2, max=60, jitter=5),
    stop=stop_after_attempt(5)
)
def ask_gemini(resume_text):
    """Calls Gemini 2.5 Flash using the new GenAI SDK."""
    prompt = f"""
    Act as an expert Senior Technical Recruiter. Analyze the following resume:
    
    {resume_text}
    
    ---
    Format the output in Markdown with these headers:
    ## 📄 Professional Profile
    ## 🛠️ Critical Skill Gaps
    ## 🚀 6-Month Preparation Roadmap
    """
    
    try:
        # UPDATED MODEL ID FOR 2.5 FLASH
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# --- API Routes ---

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    
    try:
        text = extract_text_from_pdf(file)
        analysis = ask_gemini(text)
        return jsonify({"analysis": analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server starting on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)