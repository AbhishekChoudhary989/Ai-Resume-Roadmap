from flask import Flask, request, jsonify
from flask_cors import CORS
from src.helper import extract_text_from_pdf, ask_gemini
import os

# --- 1. INITIALIZE APP ---
app = Flask(__name__)
CORS(app)  # Allow frontend to connect

@app.route('/')
def home():
    return "Backend is running successfully! 🚀"

# --- 2. STRICT VALIDATION FUNCTION (The Gatekeeper) ---
def validate_document(text):
    """
    Validates if the document is a resume.
    Refuses: Source Code, Bills, Government Forms, Logs, Practical files.
    """
    text_lower = text.lower()
    
    # 🚫 RED FLAG KEYWORDS (Immediate Rejection List)
    red_flags = [
        # --- FINANCIAL & GOVT (Bills, Tickets, PF, Taxes) ---
        "employees' provident fund", "epf scheme", "uan based", "claim form",
        "tax invoice", "bill of supply", "gstin", "total amount", 
        "reservation slip", "pnr no", "railway", "transaction id", 
        "bank statement", "account summary", "credit card", "payment receipt",
        
        # --- IT / CODING JUNK (Source Code, Logs, Configs) ---
        "public class", "public static void", "def __init__", "import react", 
        "console.log", "<!doctype html>", "<html>", "<body>", 
        "exception in thread", "stack trace", "error: ", "warning: ",
        "npm install", "yarn add", "pip install", "django.db", 
        "return 0;", "std::cout", "#include <", "void main(",
        
        # --- ACADEMIC / STUDENT (Lab Manuals, Practicals) ---
        "practical list", "lab manual", "experiment no", "aim:", 
        "conclusion:", "observation table", "submitted to:", 
        "teacher's signature", "index no", "college of engineering"
    ]
    
    # 1. Check Python Keywords (Fastest)
    for flag in red_flags:
        if flag in text_lower:
            return f"REJECT: Detected '{flag}' - This looks like a non-resume document (Code, Bill, or Practical)."

    # 2. Check Length (Resumes are rarely < 100 chars or > 30k chars)
    if len(text) < 100:
        return "REJECT: Document is too short/empty to be a valid resume."
    if len(text) > 30000: 
        return "REJECT: Document is too long (likely a book, log file, or thesis)."

    # 3. Check with Gemini (Smart Context Check)
    filter_prompt = f"""
    You are a strict Document Validator. 
    Analyze the text below. Is it a Professional Resume/CV?
    
    STRICT RULES:
    - If it is Source Code (Java, Python, React, etc.) -> REJECT.
    - If it is a Log File, Error Trace, or Config -> REJECT.
    - If it is a Government Form, Ticket, Invoice, or Receipt -> REJECT.
    - It MUST contain a "Skills", "Experience", or "Education" section to be VALID.
    
    RESPONSE FORMAT:
    - If Valid Resume: Output ONLY "VALID"
    - If Invalid: Output "REJECT: <Reason>"
    
    ---------------------
    DOCUMENT TEXT SAMPLE:
    {text[:2000]}
    ---------------------
    """
    return ask_gemini(filter_prompt).strip()

# --- 3. MAIN API ROUTE ---
@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    
    try:
        # A. Extract Text
        text = extract_text_from_pdf(file)
        
        # B. Run Validation (Filter)
        validation_result = validate_document(text)
        
        # C. Check for Rejection
        if "VALID" not in validation_result:
            # Clean up the error message for the user
            error_msg = validation_result.replace("REJECT:", "").strip()
            if "REJECT" in error_msg: error_msg = "Document is not a valid resume."
            
            print(f"🚫 BLOCKED: {error_msg}")  # Log to terminal
            return jsonify({
                "error": f"⚠️ Upload Failed: {error_msg}"
            }), 400

        # D. Run Analysis (Only if Valid)
        analysis_prompt = f"""
        You are an expert Senior Technical Recruiter. The user has uploaded a verified resume.
        Generate a strict, high-value career roadmap in Markdown.
        
        RESUME TEXT:
        {text}
        
        OUTPUT FORMAT (Markdown):
        
        ## 📄 Professional Profile
        *Write a compelling 3-4 sentence professional summary.*
        
        ## 🛠️ Technical Skills Analysis
        *List the key skills found, categorized by Frontend, Backend, Database, Tools, etc.*
        
        ## 📉 Critical Skill Gaps
        *Create a Markdown Table with two columns: "Missing Skill" and "Why it is needed". Identify missing modern technologies.*
        
        ## 🚀 Career Roadmap (Next 6 Months)
        *Create a step-by-step list of projects or certifications to reach the next level.*
        
        ## ⚖️ Final Verdict
        *Assess if they are Junior/Mid/Senior and their best job fit.*
        """
        
        analysis = ask_gemini(analysis_prompt)
        return jsonify({"analysis": analysis})
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)