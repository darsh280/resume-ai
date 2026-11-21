import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000',
});

// Dashboard
export const getDashboardStats = () => API.get('/api/dashboard/stats');

// Jobs
export const createJob = (data) => API.post('/api/jobs', data);
export const listJobs = () => API.get('/api/jobs');
export const getJob = (id) => API.get(`/api/jobs/${id}`);
export const uploadJDFile = (file) => {
  const fd = new FormData();
  fd.append('file', file);
  return API.post('/api/jobs/upload-jd', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

// Resumes
export const uploadResumes = (files) => {
  const fd = new FormData();
  files.forEach((f) => fd.append('files', f));
  return API.post('/api/resumes/upload', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};
export const listResumes = () => API.get('/api/resumes');

// Matching
export const analyzeResumes = (jobId, resumeIds = []) =>
  API.post('/api/matching/analyze', { job_id: jobId, resume_ids: resumeIds });

// Candidates
export const getCandidates = (params = {}) => API.get('/api/candidates', { params });
export const getCandidate = (id) => API.get(`/api/candidates/${id}`);

// History
export const getHistory = () => API.get('/api/analysis/history');

// Reports
export const exportCSV = (params = {}) =>
  API.get('/api/reports/csv', { params, responseType: 'blob' });
export const exportPDF = (candidateId) =>
  API.get(`/api/reports/pdf/${candidateId}`, { responseType: 'blob' });
