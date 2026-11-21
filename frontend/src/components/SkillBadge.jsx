export default function SkillBadge({ skill, type = 'default' }) {
  const styles = {
    matched: 'bg-emerald-50 text-emerald-700 border-emerald-200/80 font-medium',
    missing: 'bg-rose-50 text-rose-700 border-rose-200/80 font-medium',
    additional: 'bg-blue-50 text-blue-700 border-blue-200/80 font-medium',
    default: 'bg-slate-100 text-slate-700 border-slate-200 font-normal',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs border ${
        styles[type] || styles.default
      } tracking-tight transition-colors`}
    >
      {skill}
    </span>
  );
}
