import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Download,
  Mail,
  Phone,
  Briefcase,
  GraduationCap,
  Award,
  Sparkles,
  CheckCircle2,
  XCircle,
  PlusCircle,
  FileText,
  Info,
} from 'lucide-react';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { getCandidate, exportPDF } from '../services/api';
import ScoreBar from '../components/ScoreBar';
import SkillBadge from '../components/SkillBadge';
import LoadingSpinner from '../components/LoadingSpinner';

export default function CandidateDetails() {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    fetchCandidate();
  }, [id]);

  const fetchCandidate = async () => {
    setLoading(true);
    try {
      const res = await getCandidate(id);
      setCandidate(res.data);
    } catch {
      setCandidate(null);
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    setDownloading(true);
    try {
      const res = await exportPDF(id);
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = `candidate_${candidate?.candidate_name?.replace(/\s+/g, '_') || id}_report.pdf`;
      a.click();
    } catch {
      alert('Failed to generate PDF. Make sure reportlab is installed.');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner size="lg" text="Generating comprehensive candidate analysis..." />;
  }

  if (!candidate) {
    return (
      <div className="text-center py-20 bg-white rounded-2xl border border-slate-200">
        <p className="text-sm text-slate-500">Candidate ranking not found.</p>
        <Link to="/rankings" className="text-xs font-semibold text-blue-600 hover:underline mt-2 inline-block">
          ← Back to Candidate Rankings
        </Link>
      </div>
    );
  }

  const radarData = [
    { subject: 'Semantic', value: candidate.semantic_score || 0 },
    { subject: 'Skills', value: candidate.skill_score || 0 },
    { subject: 'Experience', value: candidate.experience_score || 0 },
    { subject: 'Education', value: candidate.education_score || 0 },
  ];

  const recBadgeColors = {
    'Excellent Match': 'bg-emerald-50 text-emerald-700 border-emerald-200',
    'Good Match': 'bg-blue-50 text-blue-700 border-blue-200',
    'Moderate Match': 'bg-amber-50 text-amber-700 border-amber-200',
    'Low Match': 'bg-rose-50 text-rose-700 border-rose-200',
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Back button and title */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link
            to="/rankings"
            className="p-2 rounded-xl bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 transition"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                {candidate.candidate_name || 'Candidate Profile'}
              </h1>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                Rank #{candidate.rank}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Source file: {candidate.filename}
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={handleExportPDF}
          disabled={downloading}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition shadow-sm disabled:opacity-50"
        >
          <Download className="w-3.5 h-3.5 text-slate-500" />
          <span>{downloading ? 'Generating PDF...' : 'Download PDF Report'}</span>
        </button>
      </div>

      {/* Top Profile & Radar Chart Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center font-bold text-lg shadow-md shadow-blue-500/20">
                {candidate.candidate_name ? candidate.candidate_name.charAt(0) : 'C'}
              </div>
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  {candidate.candidate_name}
                </h3>
                <span
                  className={`inline-block mt-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold border ${
                    recBadgeColors[candidate.recommendation] || 'bg-slate-100 text-slate-700'
                  }`}
                >
                  {candidate.recommendation}
                </span>
              </div>
            </div>

            <div className="space-y-2.5 text-xs text-slate-600 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                <span className="truncate">{candidate.email || 'Not provided'}</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-3.5 h-3.5 text-slate-400" />
                <span>{candidate.phone || 'Not provided'}</span>
              </div>
              <div className="flex items-center gap-2">
                <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                <span>{candidate.years_experience ? `${candidate.years_experience} years estimated exp` : '0 years exp'}</span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 text-center">
            <span className="text-[11px] text-slate-400">Overall Match Score</span>
            <div className="text-3xl font-extrabold text-blue-600 font-mono mt-0.5">
              {candidate.final_score?.toFixed(1)}%
            </div>
          </div>
        </div>

        {/* Score Component Breakdown Progress */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
              Weighted Component Breakdown
            </h3>
            <div className="space-y-4">
              <ScoreBar
                label="Semantic Similarity"
                score={candidate.semantic_score}
                weight="40%"
                color="indigo"
              />
              <ScoreBar
                label="Technical Skill Match"
                score={candidate.skill_score}
                weight="35%"
                color="blue"
              />
              <ScoreBar
                label="Relevant Experience"
                score={candidate.experience_score}
                weight="15%"
                color="emerald"
              />
              <ScoreBar
                label="Education & Qualification"
                score={candidate.education_score}
                weight="10%"
                color="purple"
              />
            </div>
          </div>
          <p className="text-[10px] text-slate-400 mt-4 leading-normal">
            Formula: (Semantic × 0.40) + (Skills × 0.35) + (Experience × 0.15) + (Education × 0.10)
          </p>
        </div>

        {/* Radar Chart Visual */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col items-center justify-between">
          <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider w-full text-left mb-2">
            Skill & Semantic Radar
          </h3>
          <div className="w-full h-48">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10, fill: '#64748b' }} />
                <Radar
                  name="Score"
                  dataKey="value"
                  stroke="#4f46e5"
                  fill="#4f46e5"
                  fillOpacity={0.25}
                />
                <Tooltip
                  formatter={(value) => [`${value.toFixed(1)}%`, 'Score']}
                  contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', fontSize: '11px' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <span className="text-[10px] text-slate-400 text-center">
            Multi-axis normalized evaluation
          </span>
        </div>
      </div>

      {/* Skills Analysis Section: Matched, Missing, Additional */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Matched Skills */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2 text-emerald-700">
            <CheckCircle2 className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider">
              Matched Skills ({candidate.matched_skills?.length || 0})
            </h3>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {candidate.matched_skills?.map((s) => (
              <SkillBadge key={s} skill={s} type="matched" />
            ))}
            {!candidate.matched_skills?.length && (
              <span className="text-xs text-slate-400">No overlapping skills found.</span>
            )}
          </div>
        </div>

        {/* Missing Skills */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2 text-rose-700">
            <XCircle className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider">
              Missing Skills ({candidate.missing_skills?.length || 0})
            </h3>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {candidate.missing_skills?.map((s) => (
              <SkillBadge key={s} skill={s} type="missing" />
            ))}
            {!candidate.missing_skills?.length && (
              <span className="text-xs text-emerald-600 font-medium">All required skills matched!</span>
            )}
          </div>
        </div>

        {/* Additional Skills */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2 text-blue-700">
            <PlusCircle className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider">
              Additional Skills ({candidate.additional_skills?.length || 0})
            </h3>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {candidate.additional_skills?.map((s) => (
              <SkillBadge key={s} skill={s} type="additional" />
            ))}
            {!candidate.additional_skills?.length && (
              <span className="text-xs text-slate-400">None detected.</span>
            )}
          </div>
        </div>
      </div>

      {/* Extracted Sections from Resume: Education, Experience, Projects, Certifications */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
        <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
          Extracted Resume Details
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Work Experience */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
              <Briefcase className="w-3.5 h-3.5 text-blue-600" />
              <span>Work Experience</span>
            </div>
            {candidate.work_experience?.length > 0 ? (
              <ul className="text-xs text-slate-600 space-y-1.5 list-disc list-inside bg-slate-50 p-3.5 rounded-xl border border-slate-100 max-h-48 overflow-y-auto">
                {candidate.work_experience.map((w, idx) => (
                  <li key={idx} className="leading-relaxed">{w}</li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400 italic">No explicit experience section detected.</p>
            )}
          </div>

          {/* Education */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
              <GraduationCap className="w-3.5 h-3.5 text-purple-600" />
              <span>Education</span>
            </div>
            {candidate.education?.length > 0 ? (
              <ul className="text-xs text-slate-600 space-y-1.5 list-disc list-inside bg-slate-50 p-3.5 rounded-xl border border-slate-100 max-h-48 overflow-y-auto">
                {candidate.education.map((e, idx) => (
                  <li key={idx} className="leading-relaxed">{e}</li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400 italic">No explicit education section detected.</p>
            )}
          </div>

          {/* Projects */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
              <FileText className="w-3.5 h-3.5 text-emerald-600" />
              <span>Projects</span>
            </div>
            {candidate.projects?.length > 0 ? (
              <ul className="text-xs text-slate-600 space-y-1.5 list-disc list-inside bg-slate-50 p-3.5 rounded-xl border border-slate-100 max-h-48 overflow-y-auto">
                {candidate.projects.map((p, idx) => (
                  <li key={idx} className="leading-relaxed">{p}</li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400 italic">No explicit projects section detected.</p>
            )}
          </div>

          {/* Certifications */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
              <Award className="w-3.5 h-3.5 text-amber-600" />
              <span>Certifications</span>
            </div>
            {candidate.certifications?.length > 0 ? (
              <ul className="text-xs text-slate-600 space-y-1.5 list-disc list-inside bg-slate-50 p-3.5 rounded-xl border border-slate-100 max-h-48 overflow-y-auto">
                {candidate.certifications.map((c, idx) => (
                  <li key={idx} className="leading-relaxed">{c}</li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400 italic">No explicit certifications section detected.</p>
            )}
          </div>
        </div>
      </div>

      {/* AI Explanation Banner */}
      <div className="p-5 rounded-2xl bg-indigo-50/70 border border-indigo-200/80 text-xs text-indigo-950 space-y-1.5">
        <div className="flex items-center gap-2 font-bold text-indigo-900">
          <Sparkles className="w-4 h-4 text-indigo-600" />
          <span>Explainable Ranking Rationale</span>
        </div>
        <p className="leading-relaxed text-indigo-900/80">
          <strong>{candidate.candidate_name}</strong> earned a composite score of{' '}
          <strong>{candidate.final_score?.toFixed(1)}%</strong> ({candidate.recommendation}).
          Semantic embeddings from SentenceTransformers generated a similarity of{' '}
          <strong>{candidate.semantic_score?.toFixed(1)}%</strong> (40% weight).
          The candidate satisfied{' '}
          <strong>{candidate.matched_skills?.length || 0}</strong> required technical skills with{' '}
          <strong>{candidate.missing_skills?.length || 0}</strong> skill gaps (35% weight).
          Relevant work experience scored <strong>{candidate.experience_score?.toFixed(1)}%</strong> (15% weight)
          and educational background scored <strong>{candidate.education_score?.toFixed(1)}%</strong> (10% weight).
        </p>
      </div>
    </div>
  );
}
