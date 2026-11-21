import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

export default function Layout() {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Header Bar */}
        <header className="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">AI Matching Engine Online</span>
          </div>
          <div className="flex items-center gap-4 text-xs text-slate-600">
            <span className="bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200 font-mono">Backend: http://localhost:8000</span>
            <span className="bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-md border border-indigo-200 font-medium">Model: all-MiniLM-L6-v2</span>
          </div>
        </header>

        {/* Page Content Container */}
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
