'use client';

import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Loader2, Sparkles, FileText, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: any) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
      setError("");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      // Connecting to Python Backend
      const res = await axios.post("http://127.0.0.1:5000/analyze-resume", formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError("Backend not connected. Make sure python backend.py is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <h1>🚀 AI Career Architect</h1>
      </nav>

      <div className="main-content">
        <motion.div 
          initial={{ opacity: 0, y: 20 }} 
          animate={{ opacity: 1, y: 0 }} 
          transition={{ duration: 0.5 }}
          className="upload-card"
        >
          <h2>Resume Analysis & Roadmap</h2>
          <p>Upload your resume to uncover skill gaps and get a personalized career path.</p>
          
          <div className="file-input-wrapper">
            <input type="file" id="resume-upload" accept=".pdf" onChange={handleFileChange} />
            <label htmlFor="resume-upload" className="file-label">
              {file ? (
                <>
                  <FileText size={48} className="text-blue-400 mb-2" />
                  <span style={{color: '#fff'}}>{file.name}</span>
                  <span style={{fontSize: '0.8rem', color: '#94a3b8'}}>(Ready to analyze)</span>
                </>
              ) : (
                <>
                  <Upload size={48} />
                  <span>Drop your PDF here or click to browse</span>
                </>
              )}
            </label>
          </div>

          {error && (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              className="error-msg"
            >
              {error}
            </motion.div>
          )}

          <button className="analyze-btn" onClick={handleUpload} disabled={loading}>
            {loading ? (
              <><Loader2 className="spin" /> Analyzing...</>
            ) : (
              <><Sparkles size={20}/> Analyze My Career</>
            )}
          </button>
        </motion.div>

        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 40 }} 
            animate={{ opacity: 1, y: 0 }} 
            transition={{ duration: 0.6 }}
            className="results-section"
          >
            <div className="result-card">
              <div className="markdown-content">
                <ReactMarkdown 
                  children={result.analysis} 
                  remarkPlugins={[remarkGfm]} 
                />
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}