import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  FileText,
  Users,
  TrendingUp,
  Award,
  Plus,
  Clock,
  ArrowRight,
  Upload,
  Brain,
  CheckCircle2,
} from 'lucide-react';
import { getDashboardStats } from '../services/api';
import StatCard from '../components/StatCard';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await getDashboardStats();
      setStats(res.data);
    } catch {
      setStats({
        total_resumes: 0,
        total_candidates: 0,
        avg_score: 0,
        top_candidate: '',
        recent_analyses: [],
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner size="lg" text="Loading recruiter dashboard..." />;
  }

  return (
    <div className="space-y-8">
      {/* Top Banner / Welcome */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Recruiter Overview
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time candidate metrics, semantic similarity rankings, and skill insights.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/upload"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors shadow-sm"
          >
            <Upload className="w-3.5 h-3.5 text-slate-500" />
            Upload Resumes
          </Link>
          <Link
            to="/new-analysis"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md shadow-blue-500/20"
          >
            <Plus className="w-3.5 h-3.5" />
            New Job Analysis
          </Link>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          icon={FileText}
          label="Total Resumes Uploaded"
          value={stats?.total_resumes ?? 0}
          color="blue"
          subtitle="Processed in database"
        />
        <StatCard
          icon={Users}
          label="Candidates Ranked"
          value={stats?.total_candidates ?? 0}
          color="purple"
          subtitle="Evaluated across jobs"
        />
        <StatCard
          icon={TrendingUp}
          label="Average Match Score"
          value={`${stats?.avg_score?.toFixed(1) ?? '0.0'}%`}
          color="emerald"
          subtitle="Weighted AI score"
        />
        <StatCard
          icon={Award}
          label="Top Matched Candidate"
          value={stats?.top_candidate || 'None yet'}
          color="amber"
          subtitle="Highest ranked profile"
        />
      </div>

      {/* Main Content: Recent Analyses & Scoring Formula Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Analysis History */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-slate-400" />
              <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
                Recent Analysis Sessions
              </h2>
            </div>
            <Link
              to="/history"
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
            >
              View all <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {stats?.recent_analyses?.length > 0 ? (
            <div className="divide-y divide-slate-100">
              {stats.recent_analyses.map((a) => (
                <div
                  key={a.id}
                  className="py-3.5 flex items-center justify-between hover:bg-slate-50/50 rounded-xl px-2 transition-colors"
                >
                  <div className="min-w-0 pr-4">
                    <p className="text-sm font-semibold text-slate-800 truncate">
                      {a.name}
                    </p>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {a.total_resumes} resumes analyzed •{' '}
                      {a.created_at
                        ? new Date(a.created_at).toLocaleDateString()
                        : 'Recent'}
                    </p>
                  </div>
                  <div className="flex items-center gap-4 shrink-0">
                    <div className="text-right">
                      <span className="text-xs font-bold text-emerald-600 font-mono">
                        {a.avg_score?.toFixed(1)}%
                      </span>
                      <p className="text-[10px] text-slate-400">Avg Score</p>
                    </div>
                    <Link
                      to="/rankings"
                      className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-blue-50 hover:text-blue-600 text-slate-700 transition-colors"
                    >
                      View Rankings
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-slate-400 text-xs">
              <p>No analysis sessions recorded yet.</p>
              <Link
                to="/new-analysis"
                className="text-blue-600 hover:underline font-semibold mt-1 inline-block"
              >
                Create your first job analysis →
              </Link>
            </div>
          )}
        </div>

        {/* Explainable Scoring Methodology Box */}
        <div className="bg-gradient-to-br from-[#0a192f] to-[#172a45] text-white rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Brain className="w-5 h-5 text-indigo-400" />
              <h3 className="font-bold text-sm tracking-wide">
                Explainable AI Scoring
              </h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              All candidate rankings are computed transparently via an explainable 4-component weighted model:
            </p>

            <div className="space-y-2.5 text-xs">
              <div className="flex items-center justify-between p-2 rounded-lg bg-white/5 border border-white/10">
                <span className="text-slate-300">Semantic Similarity (all-MiniLM-L6-v2)</span>
                <span className="font-bold text-indigo-400 font-mono">40%</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-white/5 border border-white/10">
                <span className="text-slate-300">Technical Skill Match %</span>
                <span className="font-bold text-blue-400 font-mono">35%</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-white/5 border border-white/10">
                <span className="text-slate-300">Relevant Experience</span>
                <span className="font-bold text-emerald-400 font-mono">15%</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-white/5 border border-white/10">
                <span className="text-slate-300">Education & Qualification</span>
                <span className="font-bold text-purple-400 font-mono">10%</span>
              </div>
            </div>
          </div>

          <div className="pt-4 mt-4 border-t border-white/10 flex items-center gap-2 text-[11px] text-slate-400">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            <span>Zero hardcoded mock scores • 100% computed</span>
          </div>
        </div>
      </div>
    </div>
  );
}
