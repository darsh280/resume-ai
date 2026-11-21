export default function StatCard({ icon: Icon, label, value, color = 'blue', subtitle }) {
  const colorMap = {
    blue: {
      bg: 'bg-blue-50 text-blue-600 border-blue-100',
      gradient: 'from-blue-600 to-indigo-600',
    },
    purple: {
      bg: 'bg-purple-50 text-purple-600 border-purple-100',
      gradient: 'from-purple-600 to-indigo-600',
    },
    emerald: {
      bg: 'bg-emerald-50 text-emerald-600 border-emerald-100',
      gradient: 'from-emerald-600 to-teal-600',
    },
    amber: {
      bg: 'bg-amber-50 text-amber-600 border-amber-100',
      gradient: 'from-amber-500 to-orange-500',
    },
  };

  const scheme = colorMap[color] || colorMap.blue;

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow duration-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold tracking-wider text-slate-500 uppercase">{label}</p>
          <p className="text-2xl font-bold text-slate-900 mt-1 tracking-tight">{value}</p>
          {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3.5 rounded-2xl border ${scheme.bg}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}
