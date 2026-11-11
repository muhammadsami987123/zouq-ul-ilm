"use client";
import { useEffect, useMemo, useRef, useState } from 'react';
import { FaFileAlt, FaSpinner, FaDownload, FaCheck, FaPlus, FaUndo } from 'react-icons/fa';
import api from '@/lib/api';
import { API_URL } from '@/lib/config';

export default function NotesPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [topics, setTopics] = useState<string[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [manualTopic, setManualTopic] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [progress, setProgress] = useState(0);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [genConfig, setGenConfig] = useState({
    temperature: 0.4,
    top_k: 50,
    top_p: 0.9,
    max_output_tokens: 800,
  });

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
            if (data.status === 'completed') {
              setIsGenerating(false);
              setIsComplete(true);
              if (interval) window.clearInterval(interval);
            } else if (data.status === 'failed') {
              setError(data.error || 'Unknown error');
              setIsGenerating(false);
              if (interval) window.clearInterval(interval);
            }
          }
        } catch (e: any) {
          setError(e?.message || 'Progress check failed');
        }
      }, 2000) as unknown as number;
    }
    return () => {
      if (interval) window.clearInterval(interval);
    };
  }, [isGenerating, taskId]);

  const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setIsComplete(false);
    setError(null);
    const form = new FormData();
    form.append('pdf', f);
    const res = await fetch(`${API_URL}/upload`, { method: 'POST', body: form });
    const data = await res.json();
    if (res.ok) {
      setFileId(data.fileId);
      const extracted = data.topics || [];
      setTopics(extracted);
      setSelectedTopics(extracted);
    } else {
      setError(data.error || 'Failed to upload file');
    }
  };

  const toggleTopic = (topic: string) => {
    setSelectedTopics(prev => prev.includes(topic) ? prev.filter(t => t !== topic) : [...prev, topic]);
  };

  const addManualTopic = (e: React.FormEvent) => {
    e.preventDefault();
    const t = manualTopic.trim();
    if (!t) return;
    setTopics(prev => (prev.includes(t) ? prev : [...prev, t]));
    setSelectedTopics(prev => (prev.includes(t) ? prev : [...prev, t]));
    setManualTopic('');
  };

  const handleGenerate = async () => {
    if (!fileId && selectedTopics.length === 0) {
      setError('Please upload a PDF or enter at least one topic.');
      return;
    }
    setIsGenerating(true);
    setIsComplete(false);
    setProgress(0);
    setError(null);
    try {
      // Only send fields that are present
      const data = await api.generateNotes(
        fileId || '',
        selectedTopics,
        genConfig
      );
      if (data?.taskId) {
        setTaskId(data.taskId);
      } else {
        setIsGenerating(false);
        setError('Backend did not return taskId. Is /generate implemented?');
      }
    } catch (e: any) {
      setIsGenerating(false);
      setError(e?.message || 'Failed to start notes generation');
    }
  };

  const handleReset = () => {
    setFile(null);
    setFileId(null);
    setTopics([]);
    setSelectedTopics([]);
    setManualTopic('');
    setIsGenerating(false);
    setIsComplete(false);
    setProgress(0);
    setTaskId(null);
    setStatusMessage('');
    setError(null);
    const input = document.getElementById('fileInput') as HTMLInputElement | null;
    if (input) input.value = '';
  };

  const handleDownload = async () => {
    if (!taskId) return;
    await api.download(taskId, 'notes.pdf');
  };

  return (
    <div className="mt-6 mb-10">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-blue-500">Generate Smart Notes</h2>
        <p className="text-white/80">Transform your documents into comprehensive notes with AI</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          {/* Upload */}
          <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-5">
            <h5 className="text-xl font-semibold mb-3 flex items-center gap-2"><FaFileAlt /> Option 2: Upload PDF</h5>
            <div className="border-2 border-dashed border-slate-600/40 rounded-xl p-6 text-center bg-black/60">
              <input type="file" accept=".pdf" className="hidden" id="fileInput" onChange={onFileChange} />
              <label htmlFor="fileInput" className="cursor-pointer inline-flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 text-white border border-blue-600 font-medium">
                {file ? 'Change PDF' : 'Select PDF'}
              </label>
              {file && <p className="text-slate-300 mt-2 break-all">{file.name}</p>}
              {fileId && (
                <button onClick={handleReset} className="ml-3 inline-flex items-center gap-2 px-3 py-2 rounded-md bg-zinc-800 border border-zinc-700 text-white/90">
                  <FaUndo /> Reset
                </button>
              )}
            </div>
          </div>

          {/* Manual topics */}
          <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-5">
            <h5 className="text-xl font-semibold mb-3">Option 1: Enter Topics Manually</h5>
            <form onSubmit={addManualTopic} className="flex gap-2">
              <input value={manualTopic} onChange={(e)=>setManualTopic(e.target.value)} placeholder="Enter a topic" className="flex-1 px-3 py-2 rounded-md bg-zinc-900 border border-zinc-700 outline-none" />
              <button type="submit" className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 text-white border border-blue-600 font-medium"><FaPlus /> Add</button>
            </form>
          </div>

          {/* Topics list */}
          {topics.length > 0 && (
            <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-5">
              <div className="flex items-center justify-between mb-3">
                <h5 className="text-xl font-semibold">Topics <span className="ml-2 text-sm text-blue-400">{selectedTopics.length}/{topics.length}</span></h5>
                <div className="flex gap-2">
                  <button onClick={() => setSelectedTopics([...topics])} className="px-3 py-1 rounded bg-blue-600 text-white border border-blue-600 text-sm">Select All</button>
                  <button onClick={() => setSelectedTopics([])} className="px-3 py-1 rounded bg-red-600 text-white border border-red-600 text-sm">Deselect All</button>
                </div>
              </div>
              <div className="max-h-72 overflow-y-auto space-y-2">
                {topics.map((t, i) => (
                  <div key={i} onClick={() => toggleTopic(t)} className={`flex items-center justify-between px-4 py-2 rounded-md border cursor-pointer transition ${selectedTopics.includes(t) ? 'border-green-500 bg-green-500/10' : 'border-zinc-700 bg-zinc-900'}`}>
                    <span className="text-sm">{t}</span>
                    <span className={`w-5 h-5 rounded-full ${selectedTopics.includes(t) ? 'bg-green-500' : 'bg-red-500'}`}></span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Advanced Settings */}
          <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-5">
            <h5 className="text-xl font-semibold mb-3">Advanced Settings</h5>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-gray-400 text-sm mb-1">Temperature</label>
                <input type="number" step="0.1" min="0" max="1"
                  className="w-full p-2 rounded-md bg-zinc-900 text-white border border-zinc-700 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  value={genConfig.temperature}
                  onChange={(e) => setGenConfig({ ...genConfig, temperature: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="block text-gray-400 text-sm mb-1">Top K</label>
                <input type="number"
                  className="w-full p-2 rounded-md bg-zinc-900 text-white border border-zinc-700 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  value={genConfig.top_k}
                  onChange={(e) => setGenConfig({ ...genConfig, top_k: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="block text-gray-400 text-sm mb-1">Top P</label>
                <input type="number" step="0.05" min="0" max="1"
                  className="w-full p-2 rounded-md bg-zinc-900 text-white border border-zinc-700 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  value={genConfig.top_p}
                  onChange={(e) => setGenConfig({ ...genConfig, top_p: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="block text-gray-400 text-sm mb-1">Max Tokens</label>
                <input type="number"
                  className="w-full p-2 rounded-md bg-zinc-900 text-white border border-zinc-700 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  value={genConfig.max_output_tokens}
                  onChange={(e) => setGenConfig({ ...genConfig, max_output_tokens: Number(e.target.value) })}
                />
              </div>
            </div>
          </div>

          {/* Generate button: enabled if file uploaded or at least one topic selected */}
          {(fileId || selectedTopics.length > 0) && (
            <div className="flex items-center gap-3">
              <button onClick={handleGenerate} disabled={isGenerating} className="px-6 py-3 rounded-md bg-blue-600 text-white border border-blue-600 font-semibold disabled:opacity-50">
                {isGenerating ? (<span className="inline-flex items-center gap-2"><FaSpinner className="animate-spin" /> Generating...</span>) : 'Generate Notes'}
              </button>
            </div>
          )}
        </div>

        {/* Right panel */}
        <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-6 min-h-[300px] flex flex-col items-center justify-center text-center">
          {isGenerating && (
            <>
              <h3 className="text-2xl font-semibold mb-4">Generating Notes...</h3>
              <div className="w-full h-3 rounded bg-zinc-800 overflow-hidden mb-2">
                <div className="h-full bg-gradient-to-r from-blue-500 to-blue-300 transition-all" style={{ width: `${progress}%` }}></div>
              </div>
              <p className="text-white/70">{progress}%</p>
              {statusMessage && <p className="text-white/60 mt-2">{statusMessage}</p>}
            </>
          )}
          {isComplete && (
            <>
              <div className="text-green-400 text-4xl mb-2"><FaCheck /></div>
              <h3 className="text-2xl font-semibold mb-2">Notes Generated!</h3>
              <button onClick={handleDownload} className="mt-2 inline-flex items-center gap-2 px-6 py-3 rounded-md bg-green-600 text-white font-semibold">
                <FaDownload /> Download PDF
              </button>
            </>
          )}
          {!isGenerating && !isComplete && (
            <>
              <div className="text-4xl text-blue-500 mb-4"><FaFileAlt /></div>
              <h3 className="text-2xl font-semibold mb-2">Ready to Generate Notes</h3>
              <p className="text-white/70">Enter topics manually and/or upload a PDF file</p>
            </>
          )}
        </div>
      </div>

      {error && (
        <div className="fixed bottom-5 right-5 bg-red-600 text-white rounded-md shadow-lg px-4 py-3">
          {error}
        </div>
      )}
    </div>
  );
}
