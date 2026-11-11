"use client";
import { useEffect, useState } from 'react';
import { FaFileWord, FaSpinner, FaDownload, FaCheck, FaUndo } from 'react-icons/fa';
import api from '@/lib/api';
import { API_URL } from '@/lib/config';

export default function SummaryPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [summaryType, setSummaryType] = useState<'short'|'medium'|'long'>('medium');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [progress, setProgress] = useState(0);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState<string | null>(null);

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
        } catch (e: any) { setError(e?.message || 'Progress check failed'); }
      }, 2000) as unknown as number;
    }
    return () => { if (interval) window.clearInterval(interval); };
  }, [isGenerating, taskId]);

  const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    setFile(f); setIsComplete(false); setError(null);
    try {
      const form = new FormData(); form.append('pdf', f);
      const res = await fetch(`${API_URL}/upload`, { method: 'POST', body: form });
      const data = await res.json();
      if (res.ok) { setFileId(data.fileId); } else { setError(data.error || 'Failed to upload file'); }
    } catch (e: any) {
      setError(e?.message || 'Failed to upload file');
    }
  };

  const handleGenerate = async () => {
    if (!fileId && !summaryType) {
      setError('Please upload a PDF or select a summary type.');
      return;
    }
    setIsGenerating(true); setIsComplete(false); setProgress(0); setError(null);
    try {
      const data = await api.generateSummary(
        fileId || '',
        summaryType,
        {
          temperature: 0.4,
          top_k: 50,
          top_p: 0.9,
          max_output_tokens: 800,
        }
      );
      if (data?.taskId) {
        setTaskId(data.taskId);
      } else {
        setIsGenerating(false);
        setError('Backend did not return taskId. Is /summary implemented?');
      }
    } catch (e: any) {
      setIsGenerating(false);
      setError(e?.message || 'Failed to start summary');
    }
  };

  const handleReset = () => {
    setFile(null); setFileId(null); setIsGenerating(false); setIsComplete(false); setProgress(0); setTaskId(null); setStatusMessage(''); setError(null);
    const input = document.getElementById('fileInput') as HTMLInputElement | null; if (input) input.value = '';
  };

  const handleDownload = async () => { if (!taskId) return; await api.download(taskId, 'summary.pdf'); };

  return (
    <div className="mt-6 mb-10">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-blue-500">AI Summary Generator</h2>
        <p className="text-white/80">Generate concise summaries from your PDF documents in seconds</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-5">
            <div className="text-center mb-4">
              <div className="flex justify-center mb-3 text-blue-500 text-4xl"><FaFileWord /></div>
              <h3 className="text-xl font-semibold">Upload Document to Summarize</h3>
              <p className="text-white/60">Upload a PDF document to generate a concise summary</p>
            </div>
              <div className="border-2 border-dashed border-slate-600/40 rounded-xl p-6 text-center bg-black/60">
              <input type="file" accept=".pdf" className="hidden" id="fileInput" onChange={onFileChange} />
              <label htmlFor="fileInput" className="cursor-pointer inline-flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 text-white border border-blue-600 font-medium">
                {file ? 'Change PDF' : 'Select PDF'}
              </label>
              {file && <div className="mt-3 inline-flex items-center gap-2 bg-slate-700/20 text-slate-300 px-3 py-2 rounded">File uploaded: <span className="font-medium break-all">{file.name}</span></div>}
              {fileId && (
                <button onClick={handleReset} className="ml-3 inline-flex items-center gap-2 px-3 py-2 rounded-md bg-zinc-800 border border-zinc-700 text-white/90"><FaUndo /> Reset</button>
              )}
            </div>

            {(fileId || summaryType) && (
              <div className="mt-5">
                <h5 className="font-semibold mb-2">Summary Length</h5>
                <div className="grid grid-cols-3 gap-2">
                  {(['short','medium','long'] as const).map(t => (
                    <button key={t} onClick={() => setSummaryType(t)} className={`px-4 py-2 rounded-md border font-medium ${summaryType===t ? 'bg-blue-600 text-white border-blue-600' : 'bg-transparent text-blue-500 border-blue-500/50'}`}>
                      {t}
                    </button>
                  ))}
                </div>

                <div className="mt-4">
                  <button onClick={handleGenerate} disabled={isGenerating} className="w-full px-4 py-3 rounded-md bg-blue-600 text-white border border-blue-600 font-semibold disabled:opacity-50">
                    {isGenerating ? (<span className="inline-flex items-center gap-2"><FaSpinner className="animate-spin" /> Generating...</span>) : 'Generate Summary'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="rounded-xl shadow-xl bg-black/60 border border-yellow-400/20 p-6 min-h-[300px] flex flex-col items-center justify-center text-center">
          {isGenerating && (
            <>
              <h3 className="text-2xl font-semibold mb-4">Generating Summary...</h3>
              <div className="w-full h-3 rounded bg-zinc-800 overflow-hidden mb-2">
                <div className="h-full bg-gradient-to-r from-yellow-400 to-yellow-300 transition-all" style={{ width: `${progress}%` }}></div>
              </div>
              <p className="text-white/70">{progress}%</p>
              {statusMessage && <p className="text-white/60 mt-2">{statusMessage}</p>}
            </>
          )}
          {isComplete && (
            <>
              <div className="text-green-400 text-4xl mb-2"><FaCheck /></div>
              <h3 className="text-2xl font-semibold mb-2">Summary Generated!</h3>
              <button onClick={handleDownload} className="mt-2 inline-flex items-center gap-2 px-6 py-3 rounded-md bg-green-600 text-white font-semibold">
                <FaDownload /> Download Summary
              </button>
            </>
          )}
          {!isGenerating && !isComplete && (
            <>
              <div className="text-4xl text-blue-400 mb-4"><FaFileWord /></div>
              <h3 className="text-2xl font-semibold mb-2">Ready to Generate Summary</h3>
              <p className="text-white/70">Upload a PDF file to get started</p>
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
