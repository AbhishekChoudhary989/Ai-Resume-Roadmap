import os
import json
import fitz  # PyMuPDF
from google import genai
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(uploaded_file):
    """
    Extracts raw text from PDF bytes efficiently using PyMuPDF.
    """
    # Read bytes and reset pointer for any potential re-reads
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0) 
    
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_search_parameters(resume_text):
    """
    Uses Gemini to determine the optimal Job Title and Location for the Indeed Scraper.
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Strict prompt to ensure valid JSON output for the scraper
    prompt = f"""
    Analyze the following resume text and identify the target Job Title and preferred Location.
    Return ONLY a valid JSON object. 
    Format: {{"job_title": "string", "location": "string"}}
    
    Resume: {resume_text[:1200]}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        # Clean markdown formatting from AI response
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"Parameter Extraction Error: {e}")
        # Reliable fallback parameters
        return {"job_title": "Frontend Developer", "location": "Remote"}

def ask_gemini(text, params):
    """
    Generates a structured 6-month career roadmap report.
    Formatted specifically for the Quartz UI redesigned dashboard.
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Structured prompt to match the Professional/Gaps/Roadmap/Salary headers
    prompt = f"""
    Act as a Senior Career Architect. Based on the resume provided, create a 
    Unified Career Intelligence Report for a {params['job_title']} in {params['location']}.
    
    Resume Text: {text[:2500]}
    
    Format the response in Markdown with these EXACT headers:
    
    # Professional Profile
    (Write a 3-sentence high-level summary of the candidate's current standing)
    
    # Critical Skill Gaps
    (Identify 4-5 specific technical skills or tools the candidate needs to master)
    
    # 6-Month Roadmap
    (Provide a month-by-month actionable plan. Use bold objectives for each month)
    
    # Market Salary Benchmark
    (Provide a realistic salary range based on current Indian market data for this role)
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Gemini Roadmap Error: {e}")
        return "## Error\nUnable to generate roadmap at this time. Please check your API limits."