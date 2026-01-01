import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor # For faster parallel execution
from src.job_api import fetch_indeed_jobs 
from src.helper import extract_text_from_pdf, extract_search_parameters, ask_gemini

load_dotenv()
app = Flask(__name__)
# CRITICAL: Allow your Next.js app (usually port 3000) to talk to Flask
CORS(app) 

# Executor for parallel processing to speed up the 30s delay
executor = ThreadPoolExecutor(max_workers=2)

@app.route('/analyze-resume', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    
    try:
        # Step 1: Extract raw text
        text = extract_text_from_pdf(file)
        
        # Step 2: Extract search params
        params = extract_search_parameters(text)

        # Step 3 & 4: RUN IN PARALLEL to save time
        job_task = executor.submit(fetch_indeed_jobs, params['job_title'], params['location'])
        ai_task = executor.submit(ask_gemini, text, params)

        return jsonify({
            "analysis": ai_task.result(),
            "live_jobs": job_task.result(),
            "extracted_params": params
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure it runs on 127.0.0.1:5000
    app.run(host='127.0.0.1', port=5000, debug=True)