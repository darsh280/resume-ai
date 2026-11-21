import { Settings as SettingsIcon, Server, Brain, Shield, Database, Sliders } from 'lucide-react';

export default function Settings() {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          System Configuration & Methodology
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Technical specifications, NLP model parameters, and database settings for ResumeAI.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Backend & DB info */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-slate-900">
            <Server className="w-4 h-4 text-blue-600" />
            <h2 className="text-sm font-bold uppercase tracking-wider">
              Backend Architecture
            </h2>
          </div>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">API Framework</span>
              <span className="font-semibold text-slate-800 font-mono">FastAPI (Python)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">ASGI Server</span>
              <span className="font-semibold text-slate-800 font-mono">Uvicorn (Port 8000)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">ORM & Database</span>
              <span className="font-semibold text-slate-800 font-mono">SQLAlchemy + SQLite</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">Document Parsing</span>
              <span className="font-semibold text-slate-800 font-mono">PyMuPDF (PDF) & python-docx</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-500">Report Engine</span>
              <span className="font-semibold text-slate-800 font-mono">ReportLab (PDF) & CSV</span>
            </div>
          </div>
        </div>

        {/* AI & NLP Model Specs */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-slate-900">
            <Brain className="w-4 h-4 text-purple-600" />
            <h2 className="text-sm font-bold uppercase tracking-wider">
              AI & NLP Specifications
            </h2>
          </div>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">Embedding Model</span>
              <span className="font-semibold text-slate-800 font-mono">all-MiniLM-L6-v2</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">Embedding Dimensions</span>
              <span className="font-semibold text-slate-800 font-mono">384 Dimensions</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">Distance Metric</span>
              <span className="font-semibold text-slate-800 font-mono">Cosine Similarity</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-500">Skill Extraction</span>
              <span className="font-semibold text-slate-800 font-mono">Curated Taxonomy & Regex</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-500">Recommendation Cutoffs</span>
              <span className="font-semibold text-slate-800 font-mono">85+ / 70+ / 50+ / &lt;50</span>
            </div>
          </div>
        </div>
      </div>

      {/* Weights and scoring details */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-slate-900">
          <Sliders className="w-4 h-4 text-indigo-600" />
          <h2 className="text-sm font-bold uppercase tracking-wider">
            Explainable Weight Distribution
          </h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-2xl font-extrabold text-indigo-600 font-mono">40%</span>
            <p className="text-xs font-semibold text-slate-700 mt-1">Semantic Similarity</p>
            <p className="text-[11px] text-slate-400 mt-0.5">SentenceTransformers</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-2xl font-extrabold text-blue-600 font-mono">35%</span>
            <p className="text-xs font-semibold text-slate-700 mt-1">Skill Matching</p>
            <p className="text-[11px] text-slate-400 mt-0.5">Matched / Required ratio</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-2xl font-extrabold text-emerald-600 font-mono">15%</span>
            <p className="text-xs font-semibold text-slate-700 mt-1">Experience</p>
            <p className="text-[11px] text-slate-400 mt-0.5">Candidate vs required yrs</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-2xl font-extrabold text-purple-600 font-mono">10%</span>
            <p className="text-xs font-semibold text-slate-700 mt-1">Education</p>
            <p className="text-[11px] text-slate-400 mt-0.5">Degree level benchmark</p>
          </div>
        </div>
      </div>
    </div>
  );
}
