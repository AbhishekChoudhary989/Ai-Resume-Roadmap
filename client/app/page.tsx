'use client';

import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Sparkles, FileText, Briefcase, ExternalLink, TrendingUp, Cpu } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [stepText, setStepText] = useState("Initializing AI...");

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    
    const steps = [
      "Analyzing Resume Patterns...",
      "Extracting Target Role...",
      "Scraping Live Indeed Jobs...",
      "Architecting Your Roadmap...",
      "Finalizing Intelligence Report..."
    ];
    
    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < steps.length - 1) {
        currentStep++;
        setStepText(steps[currentStep]);
      }
    }, 5000);

    const formData = new FormData();
    formData.append("resume", file);

    try {
      // FIX: Added 60s timeout to allow scraper to finish
      const res = await axios.post("http://127.0.0.1:5000/analyze-resume", formData, {
        timeout: 60000 
      });
      setResult(res.data);
    } catch (err) {
      console.error("Backend Error:", err);
      alert("Connection failed. Ensure backend.py is running on port 5000.");
    } finally {
      clearInterval(interval);
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#020617] text-white">
      {/* Background Effect */}
      <div className="fixed inset-0 z-0 bg-[radial-gradient(circle_at_20%_20%,rgba(14,165,233,0.15),transparent_40%),radial-gradient(circle_at_80%_80%,rgba(168,85,247,0.15),transparent_40%)]" />

      {/* 🚀 Lottie Loading Overlay */}
      <AnimatePresence>
        {loading && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-black/90 backdrop-blur-xl"
          >
            <div className="w-80 h-80">
              <DotLottieReact
                src="https://lottie.host/d6387e71-fcc5-443a-a6b4-093565e6ef51/TVe21xrn17.lottie"
                loop autoplay
              />
            </div>
            <motion.p 
              key={stepText}
              initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
              className="text-xl font-black text-sky-400 uppercase italic mt-4"
            >
              {stepText}
            </motion.p>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="relative z-10 max-w-7xl mx-auto px-6">
        <nav className="flex items-center gap-3 py-10 border-b border-white/5">
          <Cpu className="text-sky-400" size={32} />
          <h1 className="text-2xl font-black italic uppercase tracking-widest">
            Career Architect <span className="text-sky-400">AI</span>
          </h1>
        </nav>

        <main className="mt-12">
          {!result && !loading && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-slate-900/50 border border-white/10 rounded-[2.5rem] p-12 max-w-2xl mx-auto text-center backdrop-blur-md">
              <h2 className="text-3xl font-black mb-4 uppercase italic">Initialize Architecture</h2>
              <div className="relative border-2 border-dashed border-slate-700 rounded-3xl p-16 mb-8 hover:border-sky-500 transition-all cursor-pointer">
                <input 
                  type="file" className="absolute inset-0 opacity-0 cursor-pointer z-10" 
                  accept=".pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} 
                />
                <Upload size={64} className="mx-auto text-slate-600 mb-4" />
                <p className="text-slate-400 font-bold uppercase text-xs">{file ? file.name : "Inject Resume PDF"}</p>
              </div>
              <button onClick={handleUpload} className="w-full bg-sky-600 hover:bg-sky-500 py-6 rounded-2xl font-black tracking-widest flex justify-center items-center gap-3 shadow-[0_0_30px_rgba(14,165,233,0.3)]">
                <Sparkles size={24}/> START ARCHITECTURE
              </button>
            </motion.div>
          )}

          {result && (
            <div className="grid lg:grid-cols-[1fr_420px] gap-10">
              <div className="bg-slate-900/50 border border-white/10 p-10 rounded-[2rem] backdrop-blur-sm">
                <div className="prose prose-invert max-w-none prose-headings:text-sky-400">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.analysis}</ReactMarkdown>
                </div>
              </div>
              <aside className="space-y-8">
                <div className="bg-gradient-to-br from-sky-600/20 to-indigo-600/20 border border-sky-500/30 p-8 rounded-[2rem]">
                  <TrendingUp className="text-sky-400 mb-2" />
                  <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Market Alpha</p>
                  <p className="text-6xl font-black">+25-40%</p>
                </div>
                <div className="bg-slate-900/50 border border-white/10 p-8 rounded-[2rem]">
                   <h3 className="font-bold mb-6 flex items-center gap-2 italic text-sky-400 uppercase"><Briefcase size={20} /> Live Indian Nodes</h3>
                   {result.live_jobs?.map((job: any, i: number) => (
                     <div key={i} className="p-4 bg-slate-800/40 rounded-xl border border-white/5 mb-4 hover:border-sky-500 transition-all">
                       <p className="font-bold text-sm leading-tight mb-2">{job.title}</p>
                       <p className="text-[10px] text-slate-500 mb-4">{job.company}</p>
                       <a href={job.url} target="_blank" className="text-[10px] bg-sky-600 px-3 py-1.5 rounded-lg flex items-center gap-1 w-fit font-black uppercase">Apply <ExternalLink size={10} /></a>
                     </div>
                   ))}
                </div>
              </aside>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}