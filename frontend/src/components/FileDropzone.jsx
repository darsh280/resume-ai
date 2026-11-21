import { useCallback, useState } from 'react';
import { UploadCloud, FileText, X, AlertCircle } from 'lucide-react';

export default function FileDropzone({ onFilesSelected, accept = '.pdf,.docx', maxFiles = 20 }) {
  const [dragOver, setDragOver] = useState(false);
  const [files, setFiles] = useState([]);
  const [errors, setErrors] = useState([]);

  const handleFiles = useCallback(
    (newFiles) => {
      const fileList = Array.from(newFiles);
      const valid = [];
      const errs = [];

      fileList.forEach((f) => {
        const ext = f.name.split('.').pop().toLowerCase();
        if (!['pdf', 'docx'].includes(ext)) {
          errs.push(`${f.name}: Only PDF and DOCX files are allowed`);
        } else {
          valid.push(f);
        }
      });

      // Avoid duplicates in file selection by name
      const existingNames = new Set(files.map((f) => f.name));
      const deduplicated = valid.filter((f) => !existingNames.has(f.name));

      const combined = [...files, ...deduplicated].slice(0, maxFiles);
      setFiles(combined);
      setErrors(errs);
      onFilesSelected(combined);
    },
    [files, maxFiles, onFilesSelected]
  );

  const removeFile = (idx) => {
    const updated = files.filter((_, i) => i !== idx);
    setFiles(updated);
    onFilesSelected(updated);
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => document.getElementById('resume-file-input').click()}
        className={`border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all duration-200 ${
          dragOver
            ? 'border-blue-500 bg-blue-50/50 scale-[0.99]'
            : 'border-slate-300 hover:border-blue-500 hover:bg-slate-50/60 bg-white'
        }`}
      >
        <div className="mx-auto w-14 h-14 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 mb-4">
          <UploadCloud className="w-7 h-7" />
        </div>
        <p className="text-base font-semibold text-slate-800">
          Drag & drop resumes here, or <span className="text-blue-600 hover:underline">browse</span>
        </p>
        <p className="text-xs text-slate-500 mt-1.5">
          Supports PDF & DOCX • Up to {maxFiles} files in a single batch
        </p>

        <input
          id="resume-file-input"
          type="file"
          className="hidden"
          multiple
          accept={accept}
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>

      {errors.length > 0 && (
        <div className="space-y-1">
          {errors.map((e, idx) => (
            <div key={idx} className="flex items-center gap-2 text-rose-600 text-xs bg-rose-50 p-2.5 rounded-lg border border-rose-100">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{e}</span>
            </div>
          ))}
        </div>
      )}

      {files.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 divide-y divide-slate-100">
          <div className="px-4 py-2.5 bg-slate-50 rounded-t-xl text-xs font-semibold text-slate-600 flex justify-between items-center">
            <span>Selected Resumes ({files.length})</span>
            <button
              type="button"
              onClick={() => {
                setFiles([]);
                onFilesSelected([]);
              }}
              className="text-slate-400 hover:text-rose-600 text-[11px]"
            >
              Clear All
            </button>
          </div>
          <div className="max-h-56 overflow-y-auto divide-y divide-slate-100">
            {files.map((file, idx) => (
              <div key={idx} className="px-4 py-2.5 flex items-center justify-between hover:bg-slate-50/50 text-xs">
                <div className="flex items-center gap-2.5 min-w-0">
                  <FileText className="w-4 h-4 text-blue-500 shrink-0" />
                  <span className="font-medium text-slate-800 truncate">{file.name}</span>
                  <span className="text-slate-400 text-[11px] shrink-0 font-mono">
                    ({(file.size / 1024).toFixed(1)} KB)
                  </span>
                </div>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(idx);
                  }}
                  className="text-slate-400 hover:text-rose-500 p-1"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
