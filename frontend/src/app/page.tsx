import {
  FaFileAlt,
  FaFileWord,
  FaFilePowerpoint,
  FaEdit,
  FaMagic,
  FaRocket,
  FaLightbulb,
  FaGraduationCap,
} from "react-icons/fa";
import Link from "next/link";

export default function Home() {
  return (
    <div className="mt-4 mb-12">
      {/* Hero Section */}
      <div className="text-center rounded-2xl mb-12 p-8 sm:p-12 bg-gradient-to-br from-blue-500/6 via-slate-500/6 to-cyan-500/6 relative overflow-hidden">
        <div className="relative z-10 max-w-4xl mx-auto">
          <div className="mb-6 flex justify-center">
            <FaMagic className="text-5xl text-blue-500 drop-shadow-[0_0_12px_rgba(59,130,246,0.25)]" />
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold mb-4 text-blue-500 drop-shadow-lg">
            Transform Your Documents with AI
          </h1>
          <p className="text-lg sm:text-xl text-slate-200 max-w-2xl mx-auto mb-6">
            Turn boring PDFs into amazing notes, summaries, slides, and more
            with the power of AI
          </p>
          <Link
            href="/notes"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-semibold bg-blue-600 text-white border border-blue-600 shadow hover:-translate-y-0.5 transition"
          >
            {" "}
            Get Started
          </Link>
        </div>
        <div className="absolute -top-12 -right-12 w-48 h-48 rounded-full bg-blue-400/20 blur-2xl"></div>
        <div className="absolute -bottom-12 -left-12 w-48 h-48 rounded-full bg-slate-400/20 blur-2xl"></div>
      </div>

      {/* Features Section */}
      <h2 className="text-center mb-8 text-3xl font-bold text-blue-500 inline-block relative after:content-[''] after:absolute after:-bottom-2 after:left-1/2 after:-translate-x-1/2 after:w-20 after:h-[3px] after:bg-gradient-to-r after:from-blue-500 after:to-slate-400">
        <FaLightbulb className="inline mr-2 text-blue-500" /> Magical Features
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {/* Smart Notes */}
        <div className="rounded-2xl overflow-hidden shadow-xl bg-white/90 text-zinc-800 hover:-translate-y-2 transition">
          <div className="h-28 flex items-center justify-center bg-gradient-to-br from-blue-500/30 to-blue-200/20">
            <FaFileAlt className="text-4xl text-blue-700" />
          </div>
          <div className="p-5 text-center">
            <h3 className="text-xl font-bold text-blue-600 mb-2">
              Smart Notes
            </h3>
            <p className="text-sm text-zinc-600 mb-4">
              Generate comprehensive notes from your documents automatically
              using AI technology.
            </p>
            <Link
              href="/notes"
              className="inline-block px-4 py-2 rounded-full font-semibold bg-blue-600 text-white border border-blue-600 hover:-translate-y-0.5 transition"
            >
              Generate Notes
            </Link>
          </div>
        </div>

        {/* AI Summary */}
        <div className="rounded-2xl overflow-hidden shadow-xl bg-white/90 text-zinc-800 hover:-translate-y-2 transition">
          <div className="h-28 flex items-center justify-center bg-gradient-to-br from-blue-500/30 to-blue-200/20">
            <FaFileWord className="text-4xl text-blue-700" />
          </div>
          <div className="p-5 text-center">
            <h3 className="text-xl font-bold text-blue-600 mb-2">AI Summary</h3>
            <p className="text-sm text-zinc-600 mb-4">
              Get concise summaries of your documents with adjustable length
              options.
            </p>
            <Link
              href="/summary"
              className="inline-block px-4 py-2 rounded-full font-semibold bg-blue-600 text-white border border-blue-600 hover:-translate-y-0.5 transition"
            >
              Create Summary
            </Link>
          </div>
        </div>

        {/* Presentation Slides */}
        <div className="rounded-2xl overflow-hidden shadow-xl bg-white/90 text-zinc-800 hover:-translate-y-2 transition">
          <div className="h-28 flex items-center justify-center bg-gradient-to-br from-blue-500/30 to-blue-200/20">
            <FaFilePowerpoint className="text-4xl text-blue-700" />
          </div>
          <div className="p-5 text-center">
            <h3 className="text-xl font-bold text-blue-600 mb-2">
              Presentation Slides
            </h3>
            <p className="text-sm text-zinc-600 mb-4">
              Convert your documents into professional presentation slides
              automatically.
            </p>
            <Link
              href="/slides"
              className="inline-block px-4 py-2 rounded-full font-semibold bg-blue-600 text-white border border-blue-600 hover:-translate-y-0.5 transition"
            >
              Create Slides
            </Link>
          </div>
        </div>

        {/* Document Rewrite */}
        <div className="rounded-2xl overflow-hidden shadow-xl bg-white/90 text-zinc-800 hover:-translate-y-2 transition">
          <div className="h-28 flex items-center justify-center bg-gradient-to-br from-blue-500/30 to-blue-200/20">
            <FaEdit className="text-4xl text-blue-700" />
          </div>
          <div className="p-5 text-center">
            <h3 className="text-xl font-bold text-blue-600 mb-2">
              Document Rewrite
            </h3>
            <p className="text-sm text-zinc-600 mb-4">
              Improve the clarity and readability of your documents with
              AI-powered rewriting.
            </p>
            <Link
              href="/rewrite"
              className="inline-block px-4 py-2 rounded-full font-semibold bg-blue-600 text-white border border-blue-600 hover:-translate-y-0.5 transition"
            >
              Rewrite Document
            </Link>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="rounded-2xl p-8 shadow-xl bg-white/80 text-zinc-900">
        <h2 className="text-center text-3xl font-bold text-blue-600 mb-8 relative inline-block left-1/2 -translate-x-1/2">
          <FaGraduationCap className="inline mr-2 text-blue-500" /> How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="p-4 transition">
            <div className="w-12 h-12 rounded-full mx-auto mb-4 flex items-center justify-center font-bold text-lg text-white bg-blue-600 shadow">
              1
            </div>
            <h4 className="text-blue-600 font-semibold mb-1">Upload</h4>
            <p className="text-zinc-700">Upload your PDF document</p>
            <div className="w-16 h-16 rounded-full mx-auto mt-3 flex items-center justify-center bg-zinc-100 shadow">
              <FaFileAlt className="text-2xl text-blue-600" />
            </div>
          </div>
          <div className="p-4 transition">
            <div className="w-12 h-12 rounded-full mx-auto mb-4 flex items-center justify-center font-bold text-lg text-white bg-blue-600 shadow">
              2
            </div>
            <h4 className="text-blue-600 font-semibold mb-1">Process</h4>
            <p className="text-zinc-700">
              AI analyzes and processes your content
            </p>
            <div className="w-16 h-16 rounded-full mx-auto mt-3 flex items-center justify-center bg-zinc-100 shadow">
              <FaMagic className="text-2xl text-blue-600" />
            </div>
          </div>
          <div className="p-4 transition">
            <div className="w-12 h-12 rounded-full mx-auto mb-4 flex items-center justify-center font-bold text-lg text-white bg-blue-600 shadow">
              3
            </div>
            <h4 className="text-blue-600 font-semibold mb-1">Download</h4>
            <p className="text-zinc-700">
              Get your generated content instantly
            </p>
            <div className="w-16 h-16 rounded-full mx-auto mt-3 flex items-center justify-center bg-zinc-100 shadow">
              <FaRocket className="text-2xl text-blue-600" />
            </div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="text-center rounded-2xl mt-12 p-8 sm:p-12 bg-gradient-to-br from-blue-500/6 via-slate-500/6 to-cyan-500/6 relative overflow-hidden">
        <div className="relative z-10 max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-blue-500 mb-2">
            Ready to transform your documents?
          </h2>
          <p className="text-white/90 mb-6">
            Start using our AI-powered tools today and save hours of work!
          </p>
          <Link
            href="/notes"
            className="inline-flex items-center px-6 py-3 rounded-full font-semibold bg-blue-600 text-white border border-blue-600 shadow hover:-translate-y-0.5 transition"
          >
            Try It Now
          </Link>
        </div>
        <div className="absolute -top-12 -right-12 w-48 h-48 rounded-full bg-blue-400/20 blur-2xl"></div>
        <div className="absolute -bottom-12 -left-12 w-48 h-48 rounded-full bg-slate-400/20 blur-2xl"></div>
      </div>
    </div>
  );
}
