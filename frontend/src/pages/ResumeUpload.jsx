import { useState } from 'react';
import { Upload, CheckCircle2, AlertTriangle, XCircle, FileText, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import FileDropzone from '../components/FileDropzone';
import LoadingSpinner from '../components/LoadingSpinner';
import Notification from '../components/Notification';
import { uploadResumes } from '../services/api';

export default function ResumeUpload() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadResponse, setUploadResponse] = useState(null);
  const [notification, setNotification] = useState(null);

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setNotification({
        type: 'warning',
        message: 'Please select or drag-and-drop at least one resume file.',
      });
      return;
    }

    setUploading(true);
    setUploadResponse(null);

    try {
      const res = await uploadResumes(selectedFiles);
      setUploadResponse(res.data);
      if (res.data.total > 0) {
        setNotification({
          type: 'success',
          message: `Successfully processed & parsed ${res.data.total} resume(s)!`,
        });
      } else if (res.data.errors?.length > 0) {
        setNotification({
          type: 'warning',
          message: 'Files were processed, but some errors or duplicates occurred.',
        });
      }
    } catch {
      setNotification({
        type: 'error',
        message: 'Failed to upload resumes. Ensure the backend server is reachable.',
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Bulk Resume Upload
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Upload up to 20 candidate resumes (PDF or DOCX). Text, education, and skills will be parsed automatically.
        </p>
      </div>

      {notification && (
        <Notification {...notification} onClose={() => setNotification(null)} />
      )}

      {/* Upload Box */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 space-y-6 shadow-sm">
        <FileDropzone
          onFilesSelected={setSelectedFiles}
          accept=".pdf,.docx"
          maxFiles={20}
        />

        <div className="flex items-center justify-between pt-2">
          <p className="text-xs text-slate-500">
            {selectedFiles.length} file(s) queued for upload
          </p>
          <button
            type="button"
            onClick={handleUpload}
            disabled={uploading || selectedFiles.length === 0}
            className="flex items-center gap-2 py-2.5 px-6 rounded-xl text-xs font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 transition shadow-md shadow-blue-500/20"
          >
            {uploading ? (
              <LoadingSpinner size="sm" text="Parsing PDF & DOCX resumes..." />
            ) : (
              <>
                <Upload className="w-3.5 h-3.5" />
                <span>Upload & Parse Resumes</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Upload Results Summary */}
      {uploadResponse && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
              Upload Results Summary
            </h2>
            <Link
              to="/new-analysis"
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
            >
              Proceed to Matching <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="p-3.5 bg-emerald-50 border border-emerald-100 rounded-xl text-center">
              <span className="text-xl font-bold text-emerald-700 font-mono">
                {uploadResponse.total}
              </span>
              <p className="text-[11px] font-medium text-emerald-600 mt-0.5">Parsed Successfully</p>
            </div>
            <div className="p-3.5 bg-rose-50 border border-rose-100 rounded-xl text-center">
              <span className="text-xl font-bold text-rose-700 font-mono">
                {uploadResponse.errors?.length || 0}
              </span>
              <p className="text-[11px] font-medium text-rose-600 mt-0.5">Errors / Duplicates</p>
            </div>
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl text-center">
              <span className="text-xl font-bold text-slate-700 font-mono">
                {(uploadResponse.total || 0) + (uploadResponse.errors?.length || 0)}
              </span>
              <p className="text-[11px] font-medium text-slate-500 mt-0.5">Total Processed</p>
            </div>
          </div>

          {/* Uploaded items list */}
          {uploadResponse.uploaded?.length > 0 && (
            <div className="space-y-1.5 pt-2">
              <p className="text-xs font-semibold text-slate-700">Successfully Uploaded:</p>
              <div className="max-h-48 overflow-y-auto divide-y divide-slate-100 border border-slate-200 rounded-xl text-xs">
                {uploadResponse.uploaded.map((u, i) => (
                  <div key={i} className="p-2.5 flex items-center justify-between hover:bg-slate-50">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      <span className="font-semibold text-slate-800">{u.candidate_name || 'Candidate'}</span>
                      <span className="text-slate-400 font-mono">({u.filename})</span>
                    </div>
                    <span className="text-[11px] text-emerald-600 font-medium">Ready for Ranking</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Errors list */}
          {uploadResponse.errors?.length > 0 && (
            <div className="space-y-1.5 pt-2">
              <p className="text-xs font-semibold text-rose-700">Errors & Warnings:</p>
              <div className="max-h-40 overflow-y-auto divide-y divide-rose-100 border border-rose-200 rounded-xl text-xs bg-rose-50/30">
                {uploadResponse.errors.map((e, i) => (
                  <div key={i} className="p-2.5 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <XCircle className="w-4 h-4 text-rose-500" />
                      <span className="font-medium text-slate-700">{e.filename}</span>
                    </div>
                    <span className="text-rose-600 text-[11px]">{e.error}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
