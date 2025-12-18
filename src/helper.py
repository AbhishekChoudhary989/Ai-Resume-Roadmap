import os
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def ask_gemini(prompt, max_tokens=None):
    """Sends a prompt to Google Gemini and returns the response."""
    try:
        # Using the latest stable model
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # We pass the prompt. We ignore max_tokens here to keep it simple, 
        # but accepting the argument prevents the error.
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"