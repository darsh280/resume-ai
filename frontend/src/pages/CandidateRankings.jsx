import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Search,
  Download,
  ExternalLink,
  ChevronUp,
  ChevronDown,
  Users,
  Filter,
  CheckCircle2,
  Sparkles,
} from 'lucide-react';
import { getCandidates, listJobs, exportCSV } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';
import SkillBadge from '../components/SkillBadge';

function RecommendationBadge({ rec }) {
  const styles = {
    'Excellent Match': 'bg-emerald-50 text-emerald-700 border-emerald-200/80',
    'Good Match': 'bg-blue-50 text-blue-700 border-blue-200/80',
    'Moderate Match': 'bg-amber-50 text-amber-700 border-amber-200/80',
    'Low Match': 'bg-rose-50 text-rose-700 border-rose-200/80',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold border ${
        styles[rec] || 'bg-slate-100 text-slate-700 border-slate-200'
      }`}
    >
      {rec}
    </span>
  );
}

export default function CandidateRankings() {
  const [candidates, setCandidates] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [sortField, setSortField] = useState('final_score');
  const [sortDir, setSortDir] = useState('desc');
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    listJobs()
      .then((r) => setJobs(r.data))
      .catch(() => setJobs([]));
  }, []);

  useEffect(() => {
    fetchCandidates();
  }, [selectedJob]);

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedJob) params.job_id = selectedJob;
      const res = await getCandidates(params);
      setCandidates(res.data);
    } catch {
      setCandidates([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortField(field);
      setSortDir('desc');
    }
  };

  const handleExportCSV = async () => {
    setDownloading(true);
    try {
      const params = {};
      if (selectedJob) params.job_id = selectedJob;
      const res = await exportCSV(params);
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = `candidate_rankings_${new Date().toISOString().slice(0, 10)}.csv`;
      a.click();
    } catch {
      alert('Failed to export CSV. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  const filtered = candidates
    .filter((c) => {
      const q = search.toLowerCase();
      return (
        !search ||
        c.candidate_name?.toLowerCase().includes(q) ||
        c.email?.toLowerCase().includes(q) ||
        c.recommendation?.toLowerCase().includes(q)
      );
    })
    .sort((a, b) => {
      const v = sortDir === 'asc' ? 1 : -1;
      const valA = a[sortField] ?? '';
      const valB = b[sortField] ?? '';
      if (valA < valB) return -v;
      if (valA > valB) return v;
      return 0;
    });

  const SortIcon = ({ field }) => {
    if (sortField !== field) return null;
    return sortDir === 'asc' ? (
      <ChevronUp className="w-3.5 h-3.5 text-blue-600 inline ml-1" />
    ) : (
      <ChevronDown className="w-3.5 h-3.5 text-blue-600 inline ml-1" />
    );
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Candidate Rankings
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Sortable, explainable AI ranking table based on semantic similarity, skill match, experience, and education.
          </p>
        </div>
        <button
          type="button"
          onClick={handleExportCSV}
          disabled={downloading || candidates.length === 0}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition shadow-sm disabled:opacity-50"
        >
          <Download className="w-3.5 h-3.5 text-slate-500" />
          <span>{downloading ? 'Exporting...' : 'Export CSV'}</span>
        </button>
      </div>

      {/* Filters Bar */}
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search candidate name, email, recommendation..."
            className="w-full pl-9 pr-4 py-2.5 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-xs outline-none transition bg-white"
          />
        </div>
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400 shrink-0 hidden sm:block" />
          <select
            value={selectedJob}
            onChange={(e) => setSelectedJob(e.target.value)}
            className="w-full sm:w-64 px-3 py-2.5 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-xs outline-none transition bg-white"
          >
            <option value="">All Job Descriptions</option>
            {jobs.map((j) => (
              <option key={j.id} value={j.id}>
                {j.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Table Container */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        {loading ? (
          <LoadingSpinner text="Computing rankings and loading candidates..." />
        ) : filtered.length === 0 ? (
          <EmptyState
            icon={Users}
            title="No Candidates Found"
            description="Run an AI job analysis or upload more candidate resumes to view rankings."
            action={
              <Link
                to="/new-analysis"
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 text-white hover:bg-blue-700 transition"
              >
                Start New Analysis
              </Link>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/80 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-200/80">
                <tr>
                  <th
                    className="p-3.5 cursor-pointer hover:text-slate-800"
                    onClick={() => handleSort('rank')}
                  >
                    Rank <SortIcon field="rank" />
                  </th>
                  <th
                    className="p-3.5 cursor-pointer hover:text-slate-800"
                    onClick={() => handleSort('candidate_name')}
                  >
                    Candidate <SortIcon field="candidate_name" />
                  </th>
                  <th
                    className="p-3.5 cursor-pointer hover:text-slate-800"
                    onClick={() => handleSort('years_experience')}
                  >
                    Exp <SortIcon field="years_experience" />
                  </th>
                  <th
                    className="p-3.5 cursor-pointer hover:text-slate-800"
                    onClick={() => handleSort('final_score')}
                  >
                    Overall Match <SortIcon field="final_score" />
                  </th>
                  <th className="p-3.5">Matched Skills</th>
                  <th className="p-3.5">Missing Skills</th>
                  <th
                    className="p-3.5 cursor-pointer hover:text-slate-800"
                    onClick={() => handleSort('recommendation')}
                  >
                    Recommendation <SortIcon field="recommendation" />
                  </th>
                  <th className="p-3.5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filtered.map((c, idx) => {
                  const isTop3 = c.rank <= 3;
                  return (
                    <tr
                      key={c.id}
                      className="hover:bg-slate-50/60 transition-colors"
                    >
                      {/* Rank */}
                      <td className="p-3.5 whitespace-nowrap">
                        <span
                          className={`w-6 h-6 rounded-full inline-flex items-center justify-center font-bold text-[11px] font-mono ${
                            c.rank === 1
                              ? 'bg-amber-100 text-amber-800 border border-amber-300'
                              : c.rank === 2
                              ? 'bg-slate-200 text-slate-800'
                              : c.rank === 3
                              ? 'bg-amber-50 text-amber-900 border border-amber-200'
                              : 'bg-slate-100 text-slate-600'
                          }`}
                        >
                          #{c.rank}
                        </span>
                      </td>

                      {/* Name & Email */}
                      <td className="p-3.5 whitespace-nowrap">
                        <div className="font-semibold text-slate-900">
                          {c.candidate_name || 'Candidate'}
                        </div>
                        <div className="text-[11px] text-slate-400">
                          {c.email || c.filename}
                        </div>
                      </td>

                      {/* Experience */}
                      <td className="p-3.5 whitespace-nowrap font-medium text-slate-700">
                        {c.years_experience ? `${c.years_experience} yrs` : 'N/A'}
                      </td>

                      {/* Final Score */}
                      <td className="p-3.5 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-slate-900 font-mono text-sm">
                            {c.final_score?.toFixed(1)}%
                          </span>
                          <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${
                                c.final_score >= 85
                                  ? 'bg-emerald-500'
                                  : c.final_score >= 70
                                  ? 'bg-blue-500'
                                  : c.final_score >= 50
                                  ? 'bg-amber-500'
                                  : 'bg-rose-500'
                              }`}
                              style={{ width: `${c.final_score}%` }}
                            />
                          </div>
                        </div>
                      </td>

                      {/* Matched Skills */}
                      <td className="p-3.5">
                        <div className="flex flex-wrap gap-1 max-w-xs">
                          {c.matched_skills?.slice(0, 3).map((s) => (
                            <span
                              key={s}
                              className="px-1.5 py-0.5 rounded text-[10px] bg-emerald-50 text-emerald-700 border border-emerald-100"
                            >
                              {s}
                            </span>
                          ))}
                          {c.matched_skills?.length > 3 && (
                            <span className="text-[10px] text-slate-400 px-1 py-0.5">
                              +{c.matched_skills.length - 3} more
                            </span>
                          )}
                          {!c.matched_skills?.length && (
                            <span className="text-[10px] text-slate-400">None</span>
                          )}
                        </div>
                      </td>

                      {/* Missing Skills */}
                      <td className="p-3.5">
                        <div className="flex flex-wrap gap-1 max-w-xs">
                          {c.missing_skills?.slice(0, 3).map((s) => (
                            <span
                              key={s}
                              className="px-1.5 py-0.5 rounded text-[10px] bg-rose-50 text-rose-700 border border-rose-100"
                            >
                              {s}
                            </span>
                          ))}
                          {c.missing_skills?.length > 3 && (
                            <span className="text-[10px] text-slate-400 px-1 py-0.5">
                              +{c.missing_skills.length - 3}
                            </span>
                          )}
                          {!c.missing_skills?.length && (
                            <span className="text-[10px] text-emerald-600 font-medium">None</span>
                          )}
                        </div>
                      </td>

                      {/* Recommendation */}
                      <td className="p-3.5 whitespace-nowrap">
                        <RecommendationBadge rec={c.recommendation} />
                      </td>

                      {/* Action */}
                      <td className="p-3.5 text-right whitespace-nowrap">
                        <Link
                          to={`/candidates/${c.id}`}
                          className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-50 text-blue-600 hover:bg-blue-100 transition"
                        >
                          <span>Analyze</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
