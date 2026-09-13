import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import {
  History,
  FileText,
  Trash2,
  ArrowUpRight,
  Clock,
  Search,
  Sparkles,
} from 'lucide-react';

export const AnalysisHistoryPage = () => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await api.get('/analysis');
      setAnalyses(res.data);
    } catch (err) {
      console.error('Error fetching history:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this analysis record?')) return;
    try {
      await api.delete(`/analysis/${id}`);
      setAnalyses((prev) => prev.filter((a) => a.id !== id));
    } catch (err) {
      console.error('Error deleting analysis:', err);
      alert('Failed to delete analysis record.');
    }
  };

  const filteredAnalyses = analyses.filter(
    (a) =>
      a.job_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.resume_filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Analysis History</h1>
          <p className="text-xs text-slate-400 mt-1">
            Review past evaluation records, compare score evolutions, and view full reports.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative w-full sm:w-72">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
            <Search className="w-3.5 h-3.5" />
          </div>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by role or file..."
            className="w-full pl-9 pr-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-500"
          />
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        {loading ? (
          <div className="text-center py-12 text-xs text-slate-400">Loading analysis history...</div>
        ) : filteredAnalyses.length === 0 ? (
          <div className="text-center py-16 border border-dashed border-slate-800 rounded-2xl">
            <History className="w-12 h-12 text-slate-600 mx-auto mb-3" />
            <p className="text-sm font-semibold text-slate-300">
              {searchTerm ? 'No matches found' : 'No analyses generated yet'}
            </p>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-4">
              {searchTerm
                ? 'Try searching with a different job title or resume keyword.'
                : 'Upload a resume and job description to generate your first ATS evaluation.'}
            </p>
            {!searchTerm && (
              <Link
                to="/analyze"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-semibold hover:bg-teal-500/20"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Start New Analysis</span>
              </Link>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800/80 uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="pb-3 pl-2">Target Job Role</th>
                  <th className="pb-3">Resume Document</th>
                  <th className="pb-3 text-center">ATS Match</th>
                  <th className="pb-3 text-center">Resume Quality</th>
                  <th className="pb-3">Analyzed Date</th>
                  <th className="pb-3 text-right pr-2">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {filteredAnalyses.map((a) => (
                  <tr key={a.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 pl-2 font-semibold text-white">
                      {a.job_title}
                    </td>
                    <td className="py-3.5 text-slate-300 flex items-center gap-2">
                      <FileText className="w-4 h-4 text-teal-400 flex-shrink-0" />
                      <span className="truncate max-w-[200px]">{a.resume_filename}</span>
                    </td>
                    <td className="py-3.5 text-center">
                      <span className="inline-block px-2.5 py-1 rounded-full text-xs font-bold bg-teal-500/10 text-teal-400 border border-teal-500/20">
                        {a.ats_score.toFixed(0)}%
                      </span>
                    </td>
                    <td className="py-3.5 text-center">
                      <span className="inline-block px-2.5 py-1 rounded-full text-xs font-bold bg-sky-500/10 text-sky-400 border border-sky-500/20">
                        {a.resume_score.toFixed(0)}/100
                      </span>
                    </td>
                    <td className="py-3.5 text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-slate-500" />
                        <span>{new Date(a.created_at).toLocaleDateString()}</span>
                      </div>
                    </td>
                    <td className="py-3.5 text-right pr-2 space-x-2">
                      <Link
                        to={`/analysis/${a.id}`}
                        className="inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-colors"
                      >
                        <span>View</span>
                        <ArrowUpRight className="w-3 h-3" />
                      </Link>
                      <button
                        onClick={() => handleDelete(a.id)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs transition-colors"
                        title="Delete record"
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
    </div>
  );
};
