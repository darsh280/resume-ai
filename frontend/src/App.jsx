import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import NewJobAnalysis from './pages/NewJobAnalysis';
import ResumeUpload from './pages/ResumeUpload';
import CandidateRankings from './pages/CandidateRankings';
import CandidateDetails from './pages/CandidateDetails';
import AnalysisHistory from './pages/AnalysisHistory';
import Settings from './pages/Settings';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="new-analysis" element={<NewJobAnalysis />} />
          <Route path="upload" element={<ResumeUpload />} />
          <Route path="rankings" element={<CandidateRankings />} />
          <Route path="candidates/:id" element={<CandidateDetails />} />
          <Route path="history" element={<AnalysisHistory />} />
          <Route path="settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
