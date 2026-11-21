import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  PlusCircle,
  Upload,
  Users,
  History,
  Settings,
  Sparkles,
  Bot
} from 'lucide-react';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/new-analysis', icon: PlusCircle, label: 'New Job Analysis' },
  { to: '/upload', icon: Upload, label: 'Bulk Resume Upload' },
  { to: '/rankings', icon: Users, label: 'Candidate Rankings' },
  { to: '/history', icon: History, label: 'Analysis History' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-[#0a192f] text-slate-100 flex flex-col h-full border-r border-slate-800 shrink-0">
      {/* Brand Header */}
      <div className="flex items-center gap-3 px-6 py-6 border-b border-slate-800/80">
        <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Bot className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-1.5">
            <h1 className="font-bold text-lg tracking-tight text-white">ResumeAI</h1>
            <span className="px-1.5 py-0.5 text-[10px] font-semibold bg-blue-500/20 text-blue-400 rounded border border-blue-500/30">NLP</span>
          </div>
          <p className="text-xs text-slate-400 font-medium">Candidate Ranking System</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 px-3 mb-2">Main Menu</div>
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                isActive
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-500/25 font-semibold'
                  : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
              }`
            }
          >
            <Icon className="w-4 h-4 shrink-0" />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer Info Box */}
      <div className="p-4 m-4 rounded-xl bg-slate-900/90 border border-slate-800 text-xs">
        <div className="flex items-center gap-2 text-indigo-400 font-medium mb-1">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Explainable AI Engine</span>
        </div>
        <p className="text-slate-400 text-[11px] leading-relaxed">
          Powered by all-MiniLM-L6-v2 embeddings & weighted skill analytics.
        </p>
      </div>
    </aside>
  );
}
