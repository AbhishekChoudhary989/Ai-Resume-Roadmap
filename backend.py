from flask import Flask, request, jsonify
from flask_cors import CORS
from src.helper import extract_text_from_pdf, ask_gemini
import os

# --- 1. Initialize the App (This was missing!) ---
app = Flask(__name__)
CORS(app)  # Allows your React frontend to connect

# --- 2. The Routes ---
@app.route('/')
def home():
    return "Backend is running successfully! 🚀"

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    
    try:
        text = extract_text_from_pdf(file)
        
        # Expert Prompt for Gemini
        prompt = f"""
        Act as an expert Senior Technical Recruiter and Career Coach. Analyze the following resume text and provide a highly detailed, structured report in Markdown format.
        
        RESUME TEXT:
        {text}
        
        ---
        
        OUTPUT FORMAT (Use Markdown):
        
        ## 📄 Professional Profile
        *Write a compelling 3-4 sentence professional summary of the candidate.*
        
        ## 🛠️ Technical Skills Analysis
        *List the key skills found, categorized by Frontend, Backend, Database, Tools, etc.*
        
        ## 📉 Critical Skill Gaps (What is Missing?)
        *Create a Markdown Table with two columns: "Missing Skill" and "Why it is needed". Identify missing modern technologies (e.g., if they know React, do they know Redux/Next.js? If they know Python, do they know Docker/AWS?).*
        
        ## 🚀 Career Roadmap (Next 6 Months)
        *Create a step-by-step list or table suggesting exactly what projects or certifications the candidate should pursue to reach a Senior or Full-Stack level.*
        
        ## ⚖️ Final Verdict
        *Give a candid assessment of where this candidate stands (Junior/Mid/Senior) and what their best job fit is right now.*
        """
        
        analysis = ask_gemini(prompt)
        
        return jsonify({"analysis": analysis})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)