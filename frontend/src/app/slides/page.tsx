"use client";
import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { FaFilePowerpoint, FaSpinner, FaDownload, FaCheck, FaPlus, FaUndo } from 'react-icons/fa';
import api from '@/lib/api'; // Corrected import
import { API_URL } from '@/lib/config';

export default function SlidesPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [topics, setTopics] = useState<string[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [title, setTitle] = useState('');
  const [template, setTemplate] = useState('');
  const [templates, setTemplates] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [progress, setProgress] = useState(0);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { (async () => { const t = await api.getTemplates(); setTemplates(t); setTemplate(t.includes('Polyhedron') ? 'Polyhedron' : t[0] || 'Polyhedron'); })(); }, []);

  useEffect(() => {
    let interval: number | undefined;
    if (isGenerating && taskId) {
      interval = window.setInterval(async () => {
        try {
          const res = await fetch(`${API_URL}/progress/${taskId}`);
          const data = await res.json();
          if (res.ok) {
            setProgress(data.progress || 0);
            setStatusMessage(data.message || '');
            if (data.status === 'completed') { setIsGenerating(false); setIsComplete(true); if (interval) window.clearInterval(interval); }
            else if (data.status === 'failed') { setError(data.error || 'Unknown error'); setIsGenerating(false); if (interval) window.clearInterval(interval); }
          }
        } catch (e: any) { setError(e?.message || 'Progress check failed'); }
      }, 2000) as unknown as number;
    }
    return () => { if (interval) window.clearInterval(interval); };
  }, [isGenerating, taskId]);

  const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    setFile(f); setIsComplete(false); setError(null);
    const form = new FormData(); form.append('pdf', f);
    const res = await fetch(`${API_URL}/upload`, { method: 'POST', body: form });
    const data = await res.json();
    if (res.ok) {
      setFileId(data.fileId);
      const extracted = data.topics || [];
      setTopics(extracted); setSelectedTopics(extracted);
      setTitle(f.name.replace(/\.[^/.]+$/, ''));
    } else { setError(data.error || 'Failed to upload file'); }
  };

  const toggleTopic = (topic: string) => { setSelectedTopics(prev => prev.includes(topic) ? prev.filter(t => t !== topic) : [...prev, topic]); };

  const handleGenerate = async () => {
    if (!fileId && selectedTopics.length === 0 && !title) {
      setError('Please upload a PDF, enter a title, or select at least one topic.');
      return;
    }
    setIsGenerating(true); setIsComplete(false); setProgress(0); setError(null);
    const payload: any = { template };
    if (fileId) payload.fileId = fileId;
    if (selectedTopics.length > 0) payload.selectedTopics = selectedTopics;
    if (title) payload.title = title;
    const res = await fetch(`${API_URL}/slides`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) { setTaskId(data.taskId); } else { setIsGenerating(false); setError(data.error || 'Failed to start slides'); }
  };

  const handleReset = () => {
    setFile(null); setFileId(null); setTopics([]); setSelectedTopics([]); setTitle(''); setIsGenerating(false); setIsComplete(false); setProgress(0); setTaskId(null); setStatusMessage(''); setError(null);
    const input = document.getElementById('fileInput') as HTMLInputElement | null; if (input) input.value = '';
  };

  const handleDownload = async () => { if (!taskId) return; await api.download(taskId, (title || 'presentation') + '.pptx'); };

  return (
    <div className="mt-6 mb-10">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-blue-500">AI Slides Generator</h2>
        <p className="text-white/80">Create professional PowerPoint presentations from your PDF documents</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-5">
            <div className="text-center mb-4">
              <div className="flex justify-center mb-3 text-4xl text-blue-600"><FaFilePowerpoint /></div>
              <h3 className="text-xl font-semibold">Create Presentation</h3>
              <p className="text-white/60">Upload a PDF and select topics to include in your slides</p>
            </div>

            <div className="border-2 border-dashed border-slate-600/40 rounded-xl p-6 text-center bg-black/60">
              <input type="file" accept=".pdf" className="hidden" id="fileInput" onChange={onFileChange} />
              <label htmlFor="fileInput" className="cursor-pointer inline-flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 text-white border border-blue-600 font-medium">
                {file ? 'Change PDF' : 'Select PDF'}
              </label>
              {file && <p className="text-slate-300 mt-2 break-all">{file.name}</p>}
              {fileId && (
                <button onClick={handleReset} className="ml-3 inline-flex items-center gap-2 px-3 py-2 rounded-md bg-zinc-800 border border-zinc-700 text-white/90"><FaUndo /> Reset</button>
              )}
            </div>

            {(fileId || title || selectedTopics.length > 0) && (
              <div className="mt-5 space-y-4">
                <div>
                  <label className="block text-sm mb-1">Presentation Title</label>
                  <input value={title} onChange={(e)=>setTitle(e.target.value)} className="w-full px-3 py-2 rounded-md bg-zinc-900 border border-zinc-700 outline-none" placeholder="Enter a title" />
                </div>
                <div>
                  <label className="block text-sm mb-1">Template</label>
                  <select value={template} onChange={(e)=>setTemplate(e.target.value)} className="w-full px-3 py-2 rounded-md bg-zinc-900 border border-zinc-700">
                    {templates.map(t => (<option key={t} value={t}>{t}</option>))}
                  </select>
                </div>
                <div>
                  <h5 className="font-semibold mb-2">Select Topics</h5>
                  <div className="max-h-64 overflow-y-auto space-y-2">
                    {topics.map((t,i)=>(
                      <div key={i} onClick={()=>setSelectedTopics(prev => prev.includes(t)? prev.filter(x=>x!==t): [...prev,t])} className={`flex items-center justify-between px-4 py-2 rounded-md border cursor-pointer transition ${selectedTopics.includes(t) ? 'border-green-500 bg-green-500/10' : 'border-zinc-700 bg-zinc-900'}`}>
                        <span className="text-sm">{t}</span>
                        <span className={`w-5 h-5 rounded-full ${selectedTopics.includes(t) ? 'bg-green-500' : 'bg-red-500'}`}></span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="text-center">
                  <button onClick={handleGenerate} disabled={isGenerating} className="px-6 py-3 rounded-md bg-blue-600 text-white border border-blue-600 font-semibold disabled:opacity-50">
                    {isGenerating ? (<span className="inline-flex items-center gap-2"><FaSpinner className="animate-spin" /> Generating Slides...</span>) : 'Generate Slides'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-6 min-h-[400px] flex flex-col items-center justify-center text-center">
          {isGenerating && (
            <>
              <h3 className="text-2xl font-semibold mb-2">Generating Slides...</h3>
              <p className="text-white/60 mb-4">Creating a beautiful presentation for you</p>
              <div className="w-full h-3 rounded bg-zinc-800 overflow-hidden mb-2">
                <div className="h-full bg-gradient-to-r from-blue-400 to-blue-500 transition-all" style={{ width: `${progress}%` }}></div>
              </div>
              <div className="text-white/70 mt-3 space-y-1">
                <p className={progress>=15 ? 'opacity-100' : 'opacity-50'}>Analyzing content</p>
                <p className={progress>=35 ? 'opacity-100' : 'opacity-50'}>Creating slide outline</p>
                <p className={progress>=60 ? 'opacity-100' : 'opacity-50'}>Formatting content</p>
                <p className={progress>=85 ? 'opacity-100' : 'opacity-50'}>Applying template</p>
              </div>
            </>
          )}
          {isComplete && (
            <>
              <div className="text-green-400 text-4xl mb-2"><FaCheck /></div>
              <h3 className="text-2xl font-semibold mb-2">Slides Generated!</h3>
              <div className="w-[250px] h-[140px] bg-white border border-zinc-200 rounded shadow mx-auto my-4 p-2">
                <div className="h-6 bg-zinc-100 rounded mb-3" />
                <div className="space-y-2">
                  <div className="h-2 bg-zinc-100 rounded w-4/5" />
                  <div className="h-2 bg-zinc-100 rounded w-4/5" />
                  <div className="h-2 bg-zinc-100 rounded w-4/5" />
                </div>
              </div>
              <button onClick={handleDownload} className="mt-2 inline-flex items-center gap-2 px-6 py-3 rounded-md bg-green-600 text-white font-semibold">
                <FaDownload /> Download Presentation
              </button>
            </>
          )}
          {!isGenerating && !isComplete && (
            <>
              <div className="text-4xl mb-4" style={{ color: '#d24726' }}><FaFilePowerpoint /></div>
              <h3 className="text-2xl font-semibold mb-2">Ready to Create Slides</h3>
              <p className="text-white/70">{file ? 'Select topics and click "Generate Slides"' : 'Upload a PDF file to get started'}</p>
              <ul className="text-white/60 mt-4 space-y-2 text-sm">
                <li>Professional slide layouts</li>
                <li>Automatic content formatting</li>
                <li>Bullet points & headers</li>
                <li>Title and section slides</li>
                <li>Clean, readable design</li>
              </ul>
            </>
          )}
        </div>
      </div>

      {error && <div className="fixed bottom-5 right-5 bg-red-600 text-white rounded-md shadow-lg px-4 py-3">{error}</div>}
    </div>
  );
}
