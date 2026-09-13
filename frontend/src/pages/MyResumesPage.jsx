import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import {
  Files,
  FileText,
  Trash2,
  Eye,
  Plus,
  Clock,
  TrendingUp,
  X,
  Sparkles,
} from 'lucide-react';

export const MyResumesPage = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [previewResume, setPreviewResume] = useState(null);
  const [previewLoading, setPreviewLoading] = useState(false);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const res = await api.get('/resumes');
      setResumes(res.data);
    } catch (err) {
      console.error('Error fetching resumes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewText = async (resumeId) => {
    setPreviewLoading(true);
    try {
      const res = await api.get(`/resumes/${resumeId}`);
      setPreviewResume(res.data);
    } catch (err) {
      console.error('Error fetching resume detail:', err);
      alert('Unable to load resume text.');
    } finally {
      setPreviewLoading(false);
    }
  };

  const handleDelete = async (resumeId) => {
    if (!window.confirm('Are you sure you want to delete this resume and its analysis history?')) {
      return;
    }
    try {
      await api.delete(`/resumes/${resumeId}`);
      setResumes((prev) => prev.filter((r) => r.id !== resumeId));
    } catch (err) {
      console.error('Error deleting resume:', err);
      alert('Failed to delete resume.');
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return '0 KB';
    const kb = bytes / 1024;
    return kb > 1024 ? `${(kb / 1024).toFixed(1)} MB` : `${kb.toFixed(0)} KB`;
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">My Resumes</h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage your uploaded resume documents and view parsed text content.
          </p>
        </div>
        <Link
          to="/analyze"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white text-xs font-semibold hover:opacity-95 shadow-lg shadow-teal-500/20"
        >
          <Plus className="w-4 h-4" />
          <span>Upload & Analyze</span>
        </Link>
      </div>

      {/* Resumes Grid/Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        {loading ? (
          <div className="text-center py-12 text-xs text-slate-400">Loading your resumes...</div>
        ) : resumes.length === 0 ? (
          <div className="text-center py-16 border border-dashed border-slate-800 rounded-2xl">
            <Files className="w-12 h-12 text-slate-600 mx-auto mb-3" />
            <p className="text-sm font-semibold text-slate-300">No resumes stored yet</p>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-4">
              Upload your first PDF resume to run job compatibility matches and track improvements.
            </p>
            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-semibold hover:bg-teal-500/20"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Upload Resume</span>
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800/80 uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="pb-3 pl-2">Filename</th>
                  <th className="pb-3">Size</th>
                  <th className="pb-3">Uploaded Date</th>
                  <th className="pb-3 text-center">Analyses Run</th>
                  <th className="pb-3 text-center">Latest ATS</th>
                  <th className="pb-3 text-right pr-2">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {resumes.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 pl-2 font-medium text-white flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-lg bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center flex-shrink-0">
                        <FileText className="w-4 h-4" />
                      </div>
                      <span className="truncate max-w-[220px]">{r.filename}</span>
                    </td>
                    <td className="py-3.5 text-slate-400">{formatFileSize(r.file_size)}</td>
                    <td className="py-3.5 text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-slate-500" />
                        <span>{new Date(r.uploaded_at).toLocaleDateString()}</span>
                      </div>
                    </td>
                    <td className="py-3.5 text-center text-slate-300 font-semibold">
                      {r.analysis_count}
                    </td>
                    <td className="py-3.5 text-center">
                      {r.latest_ats_score !== null ? (
                        <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-teal-500/10 text-teal-400 border border-teal-500/20">
                          {r.latest_ats_score.toFixed(0)}%
                        </span>
                      ) : (
                        <span className="text-slate-600">-</span>
                      )}
                    </td>
                    <td className="py-3.5 text-right pr-2 space-x-2">
                      <button
                        onClick={() => handleViewText(r.id)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs transition-colors"
                        title="View extracted text"
                      >
                        <Eye className="w-3 h-3" />
                        <span>View</span>
                      </button>
                      <button
                        onClick={() => handleDelete(r.id)}
                        className="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs transition-colors"
                        title="Delete resume"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Extracted Text Preview Modal */}
      {previewResume && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 max-w-2xl w-full shadow-2xl flex flex-col max-h-[85vh]">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2.5">
                <FileText className="w-5 h-5 text-teal-400" />
                <div>
                  <h3 className="text-sm font-bold text-white">{previewResume.filename}</h3>
                  <p className="text-[10px] text-slate-400">Extracted Text Layer (PyMuPDF)</p>
                </div>
              </div>
              <button
                onClick={() => setPreviewResume(null)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto my-4 p-4 rounded-xl bg-slate-950 border border-slate-800/80">
              <pre className="text-xs font-mono text-slate-300 whitespace-pre-wrap leading-relaxed">
                {previewResume.extracted_text}
              </pre>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setPreviewResume(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 text-slate-200 text-xs font-semibold hover:bg-slate-700"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
