"use client";
import { useEffect, useState } from 'react';
import { FaEdit, FaSpinner, FaDownload, FaCheck, FaUndo } from 'react-icons/fa';
import api from '@/lib/api'; // Corrected import
import { API_URL } from '@/lib/config';

export default function RewritePage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [progress, setProgress] = useState(0);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let interval: number | undefined;
    if (isProcessing && taskId) {
      interval = window.setInterval(async () => {
        try {
          const res = await fetch(`${API_URL}/progress/${taskId}`);
          const data = await res.json();
          if (res.ok) {
            setProgress(data.progress || 0);
            if (data.status === 'completed') { setIsProcessing(false); setIsComplete(true); if (interval) window.clearInterval(interval); }
            else if (data.status === 'failed') { setError(data.error || 'Unknown error'); setIsProcessing(false); if (interval) window.clearInterval(interval); }
          }
        } catch (e: any) { setError(e?.message || 'Progress check failed'); }
      }, 2000) as unknown as number;
    }
    return () => { if (interval) window.clearInterval(interval); };
  }, [isProcessing, taskId]);

  const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    setFile(f); setIsComplete(false); setError(null);
    const form = new FormData(); form.append('pdf', f);
    const res = await fetch(`${API_URL}/upload`, { method: 'POST', body: form });
    const data = await res.json();
    if (res.ok) { setFileId(data.fileId); } else { setError(data.error || 'Failed to upload file'); }
  };

  const handleRewrite = async () => {
    if (!fileId) {
      setError('Please upload a PDF to rewrite.');
      return;
    }
    setIsProcessing(true); setIsComplete(false); setProgress(0); setError(null);
    const res = await fetch(`${API_URL}/rewrite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fileId })
    });
    const data = await res.json();
    if (res.ok) { setTaskId(data.taskId); } else { setIsProcessing(false); setError(data.error || 'Failed to start rewrite'); }
  };

  const handleReset = () => {
    setFile(null); setFileId(null); setIsProcessing(false); setIsComplete(false); setProgress(0); setTaskId(null); setError(null);
    const input = document.getElementById('fileInput') as HTMLInputElement | null; if (input) input.value = '';
  };

  const handleDownload = async () => { if (!taskId) return; await api.download(taskId, 'rewritten.pdf'); };

  return (
    <div className="mt-6 mb-10">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-blue-500">Rewrite Document</h2>
        <p className="text-white/80">Improve the clarity and readability of your document with AI</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-5">
            <div className="text-center mb-4">
              <div className="flex justify-center mb-3 text-4xl text-blue-500"><FaEdit /></div>
              <h3 className="text-xl font-semibold">Upload Document to Rewrite</h3>
              <p className="text-white/60">Upload a PDF document to improve its clarity and readability</p>
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


            <div className="text-center mt-4">
              <button onClick={handleRewrite} disabled={isProcessing || !fileId} className="px-6 py-3 rounded-md bg-yellow-400 text-black border border-yellow-400 font-semibold disabled:opacity-50">
                {isProcessing ? (<span className="inline-flex items-center gap-2"><FaSpinner className="animate-spin" /> Rewriting...</span>) : (<span className="inline-flex items-center gap-2"><FaEdit /> Rewrite Document</span>)}
              </button>
            </div>

            {fileId && (
              <div className="text-center mt-4">
                <button onClick={handleRewrite} disabled={isProcessing} className="px-6 py-3 rounded-md bg-blue-600 text-white border border-blue-600 font-semibold disabled:opacity-50">
                  {isProcessing ? (<span className="inline-flex items-center gap-2"><FaSpinner className="animate-spin" /> Rewriting...</span>) : (<span className="inline-flex items-center gap-2"><FaEdit /> Rewrite Document</span>)}
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="rounded-xl shadow-xl bg-black/60 border border-slate-700/20 p-6 min-h-[300px] flex flex-col items-center justify-center text-center">
          {isProcessing && (
            <>
              <h3 className="text-2xl font-semibold mb-4">Rewriting Document...</h3>
              <div className="w-full h-3 rounded bg-zinc-800 overflow-hidden mb-2">
                <div className="h-full bg-gradient-to-r from-blue-500 to-blue-300 transition-all" style={{ width: `${progress}%` }}></div>
              </div>
              <p className="text-white/70">{progress}%</p>
            </>
          )}
          {isComplete && (
            <>
              <div className="text-green-400 text-4xl mb-2"><FaCheck /></div>
              <h3 className="text-2xl font-semibold mb-2">Document Rewritten!</h3>
              <button onClick={handleDownload} className="mt-2 inline-flex items-center gap-2 px-6 py-3 rounded-md bg-green-600 text-white font-semibold">
                <FaDownload /> Download Rewritten Document
              </button>
            </>
          )}
          {!isProcessing && !isComplete && (
            <>
              <div className="text-4xl text-blue-400 mb-4"><FaEdit /></div>
              <h3 className="text-2xl font-semibold mb-2">Ready to Rewrite</h3>
              <p className="text-white/70">Upload a PDF file and click "Rewrite Document" to get started</p>
            </>
          )}
        </div>
      </div>

      {error && <div className="fixed bottom-5 right-5 bg-red-600 text-white rounded-md shadow-lg px-4 py-3">{error}</div>}
    </div>
  );
}
