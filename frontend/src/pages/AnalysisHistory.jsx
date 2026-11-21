import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { History, Calendar, Users, TrendingUp, Award, ArrowRight } from 'lucide-react';
import { getHistory } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';

export default function AnalysisHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await getHistory();
      setHistory(res.data);
    } catch {
      setHistory([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Analysis History
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Historical log of previous candidate matching sessions and average scoring benchmarks.
        </p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        {loading ? (
          <LoadingSpinner text="Loading analysis records..." />
        ) : history.length === 0 ? (
          <EmptyState
            icon={History}
            title="No Analysis History"
            description="Create a job description and run your first candidate matching analysis."
            action={
              <Link
                to="/new-analysis"
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 text-white hover:bg-blue-700 transition"
              >
                Create New Analysis
              </Link>
            }
          />
        ) : (
          <div className="divide-y divide-slate-100">
            {history.map((h) => (
              <div
                key={h.id}
                className="p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 hover:bg-slate-50/50 transition-colors"
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-blue-50 text-blue-600 rounded-xl border border-blue-100 shrink-0">
                    <History className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-sm text-slate-900">{h.name}</h3>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Target Job: <span className="font-semibold text-slate-700">{h.job_title}</span>
                    </p>
                    <div className="flex items-center gap-3 text-[11px] text-slate-400 mt-1.5">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5" />
                        {h.created_at ? new Date(h.created_at).toLocaleString() : 'N/A'}
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Users className="w-3.5 h-3.5" />
                        {h.total_resumes} resumes ranked
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-6 sm:self-center self-end">
                  <div className="text-right">
                    <span className="text-base font-extrabold text-emerald-600 font-mono">
                      {h.avg_score?.toFixed(1)}%
                    </span>
                    <p className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">
                      Average Score
                    </p>
                  </div>

                  <Link
                    to="/rankings"
                    className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-blue-50 hover:text-blue-600 transition"
                  >
                    <span>View Rankings</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
