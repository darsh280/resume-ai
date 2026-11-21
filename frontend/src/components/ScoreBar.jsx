export default function ScoreBar({ label, score = 0, weight, color = 'blue' }) {
  const safeScore = Math.max(0, Math.min(100, Number(score) || 0));

  const barColors = {
    blue: 'bg-blue-600',
    indigo: 'bg-indigo-600',
    purple: 'bg-purple-600',
    emerald: 'bg-emerald-600',
    amber: 'bg-amber-500',
    rose: 'bg-rose-500',
  };

  const selectedColor = barColors[color] || 'bg-blue-600';

  return (
    <div className="space-y-1.5">
      <div className="flex justify-between items-center text-xs">
        <span className="font-medium text-slate-700">
          {label} {weight && <span className="text-slate-400 font-normal">({weight})</span>}
        </span>
        <span className="font-bold text-slate-900 font-mono">{safeScore.toFixed(1)}%</span>
      </div>
      <div className="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden border border-slate-200/50">
        <div
          className={`h-full rounded-full transition-all duration-500 ${selectedColor}`}
          style={{ width: `${safeScore}%` }}
        />
      </div>
    </div>
  );
}
