import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Briefcase,
  Upload,
  Zap,
  CheckCircle,
  AlertCircle,
  ChevronRight,
  Sparkles,
  FileText,
} from 'lucide-react';
import { createJob, uploadJDFile, listResumes, analyzeResumes } from '../services/api';
import SkillBadge from '../components/SkillBadge';
import LoadingSpinner from '../components/LoadingSpinner';
import Notification from '../components/Notification';

export default function NewJobAnalysis() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [jobTitle, setJobTitle] = useState('');
  const [jdText, setJdText] = useState('');
  const [requiredExp, setRequiredExp] = useState('');
  const [createdJob, setCreatedJob] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [selectedResumes, setSelectedResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    if (step === 2) {
      listResumes()
        .then((r) => setResumes(r.data))
        .catch(() => setResumes([]));
    }
  }, [step]);

  const handleJDFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const r = await uploadJDFile(file);
      setJdText(r.data.content);
      setNotification({
        type: 'success',
        message: `Loaded job description from ${file.name}`,
      });
    } catch {
      setNotification({
        type: 'error',
        message: 'Failed to read JD file. Make sure it is a valid text file.',
      });
    }
  };

  const handleCreateJob = async () => {
    if (!jobTitle.trim() || !jdText.trim()) {
      setNotification({
        type: 'warning',
        message: 'Please enter both Job Title and Job Description.',
      });
      return;
    }
    setLoading(true);
    try {
      const r = await createJob({
        title: jobTitle,
        description: jdText,
        required_experience: parseFloat(requiredExp) || 0,
      });
      setCreatedJob(r.data);
      setStep(2);
      setNotification({
        type: 'success',
        message: `Extracted ${r.data.extracted_skills?.length || 0} skills from the job description!`,
      });
    } catch {
      setNotification({
        type: 'error',
        message: 'Failed to save job. Ensure the backend server is running.',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!createdJob) return;
    setLoading(true);
    try {
      const ids = selectedResumes.length > 0 ? selectedResumes : [];
      const r = await analyzeResumes(createdJob.id, ids);
      setNotification({
        type: 'success',
        message: `Matching complete! Ranked ${r.data.total_resumes} candidates.`,
      });
      setTimeout(() => navigate('/rankings'), 1000);
    } catch (err) {
      setNotification({
        type: 'error',
        message:
          err.response?.data?.detail ||
          'Analysis failed. Make sure resumes are uploaded first.',
      });
    } finally {
      setLoading(false);
    }
  };

  const toggleResume = (id) => {
    setSelectedResumes((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const selectAllResumes = () => {
    if (selectedResumes.length === resumes.length) {
      setSelectedResumes([]);
    } else {
      setSelectedResumes(resumes.map((r) => r.id));
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          New Job Description & Matching
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Define job requirements, auto-extract technical skills via NLP, and rank matching candidate resumes.
        </p>
      </div>

      {notification && (
        <Notification {...notification} onClose={() => setNotification(null)} />
      )}

      {/* Steps Bar */}
      <div className="flex items-center gap-3 bg-white p-3.5 rounded-2xl border border-slate-200">
        <div
          className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold ${
            step >= 1
              ? 'bg-blue-50 text-blue-700 border border-blue-200'
              : 'text-slate-400'
          }`}
        >
          <span className="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center text-[10px]">
            1
          </span>
          <span>Job Description & Skill Extraction</span>
        </div>
        <ChevronRight className="w-4 h-4 text-slate-300" />
        <div
          className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold ${
            step >= 2
              ? 'bg-blue-50 text-blue-700 border border-blue-200'
              : 'text-slate-400'
          }`}
        >
          <span className="w-5 h-5 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center text-[10px]">
            2
          </span>
          <span>Candidate Selection & AI Analysis</span>
        </div>
      </div>

      {step === 1 && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 space-y-6 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 space-y-2">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                Job Title <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Full Stack Developer"
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-sm outline-none transition"
              />
            </div>
            <div className="space-y-2">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                Required Experience (Years)
              </label>
              <input
                type="number"
                step="0.5"
                min="0"
                value={requiredExp}
                onChange={(e) => setRequiredExp(e.target.value)}
                placeholder="e.g. 5"
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-sm outline-none transition"
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                Job Description Text <span className="text-rose-500">*</span>
              </label>
              <label className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:text-blue-700 cursor-pointer">
                <Upload className="w-3.5 h-3.5" />
                <span>Upload .txt File</span>
                <input
                  type="file"
                  accept=".txt"
                  className="hidden"
                  onChange={handleJDFileUpload}
                />
              </label>
            </div>
            <textarea
              rows={10}
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              placeholder="Paste or upload the full job description here (including responsibilities, qualifications, technical requirements)..."
              className="w-full p-4 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-sm outline-none transition font-sans leading-relaxed"
            />
          </div>

          <button
            type="button"
            onClick={handleCreateJob}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 py-3 px-6 rounded-xl text-sm font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 transition shadow-md shadow-blue-500/20"
          >
            {loading ? (
              <LoadingSpinner size="sm" text="Extracting Skills via NLP..." />
            ) : (
              <>
                <Zap className="w-4 h-4" />
                <span>Save Job & Auto-Extract Technical Skills</span>
              </>
            )}
          </button>
        </div>
      )}

      {step === 2 && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 space-y-6 shadow-sm">
          {/* Extracted Skills Preview */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-indigo-600" />
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Extracted Job Skills ({createdJob?.extracted_skills?.length || 0})
              </h3>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {createdJob?.extracted_skills?.map((s) => (
                <SkillBadge key={s} skill={s} type="default" />
              ))}
            </div>
          </div>

          {/* Resume Selection */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-slate-800">
                  Select Resumes to Match
                </h3>
                <p className="text-xs text-slate-500">
                  Select specific candidates or analyze all available resumes.
                </p>
              </div>
              {resumes.length > 0 && (
                <button
                  type="button"
                  onClick={selectAllResumes}
                  className="text-xs font-semibold text-blue-600 hover:text-blue-700"
                >
                  {selectedResumes.length === resumes.length
                    ? 'Deselect All'
                    : 'Select All'}
                </button>
              )}
            </div>

            {resumes.length === 0 ? (
              <div className="text-center py-10 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                <FileText className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                <p className="text-xs text-slate-600 font-medium">
                  No resumes currently in the database.
                </p>
                <button
                  type="button"
                  onClick={() => navigate('/upload')}
                  className="mt-2 text-xs font-semibold text-blue-600 hover:underline"
                >
                  Go to Bulk Resume Upload →
                </button>
              </div>
            ) : (
              <div className="max-h-72 overflow-y-auto divide-y divide-slate-100 border border-slate-200 rounded-xl">
                {resumes.map((r) => {
                  const isChecked = selectedResumes.includes(r.id);
                  return (
                    <label
                      key={r.id}
                      className={`flex items-center gap-3 p-3 text-xs cursor-pointer hover:bg-slate-50 transition ${
                        isChecked ? 'bg-blue-50/40' : ''
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => toggleResume(r.id)}
                        className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                      />
                      <div className="min-w-0 flex-1">
                        <p className="font-semibold text-slate-800 truncate">
                          {r.candidate_name || r.filename}
                        </p>
                        <p className="text-[11px] text-slate-400">
                          {r.years_experience} yrs exp • {r.extracted_skills?.length || 0} skills detected
                        </p>
                      </div>
                      <span className="text-[11px] text-slate-400 font-mono">
                        {r.filename}
                      </span>
                    </label>
                  );
                })}
              </div>
            )}
          </div>

          <div className="flex items-center gap-3 pt-2">
            <button
              type="button"
              onClick={() => setStep(1)}
              className="py-2.5 px-4 rounded-xl text-xs font-semibold border border-slate-300 text-slate-700 hover:bg-slate-50 transition"
            >
              Back to Job Details
            </button>
            <button
              type="button"
              onClick={handleAnalyze}
              disabled={loading || resumes.length === 0}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 px-6 rounded-xl text-xs font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 transition shadow-md shadow-blue-500/20"
            >
              {loading ? (
                <LoadingSpinner size="sm" text="Running Semantic Embedding & Cosine Matching..." />
              ) : (
                <>
                  <Zap className="w-3.5 h-3.5" />
                  <span>
                    Run AI Matching ({selectedResumes.length > 0 ? selectedResumes.length : 'All'} Resumes)
                  </span>
                </>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
