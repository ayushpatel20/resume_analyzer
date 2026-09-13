import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import {
  Settings,
  Trash2,
  LogOut,
  AlertTriangle,
  CheckCircle2,
  X,
  ShieldAlert,
} from 'lucide-react';

export const SettingsPage = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [message, setMessage] = useState({ type: '', text: '' });
  const [showClearModal, setShowClearModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleClearHistory = async () => {
    setLoading(true);
    try {
      await api.delete('/analysis/clear-history');
      setShowClearModal(false);
      setMessage({ type: 'success', text: 'All analysis history has been successfully cleared.' });
    } catch (err) {
      console.error('Error clearing history:', err);
      setMessage({ type: 'error', text: 'Failed to clear analysis history.' });
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    setLoading(true);
    try {
      await api.delete('/auth/account');
      logout();
      navigate('/login');
    } catch (err) {
      console.error('Error deleting account:', err);
      setMessage({ type: 'error', text: 'Failed to delete account. Please try again.' });
      setLoading(false);
      setShowDeleteModal(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">System Settings</h1>
        <p className="text-xs text-slate-400 mt-1">Configure workspace preferences and manage stored history.</p>
      </div>

      {message.text && (
        <div
          className={`p-4 rounded-2xl flex items-center gap-2.5 text-xs font-medium border ${
            message.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300'
              : 'bg-rose-500/10 border-rose-500/20 text-rose-300'
          }`}
        >
          {message.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-emerald-400" />
          ) : (
            <AlertTriangle className="w-4 h-4 flex-shrink-0 text-rose-400" />
          )}
          <span>{message.text}</span>
        </div>
      )}

      {/* Data Management Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <h2 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Trash2 className="w-4 h-4 text-amber-400" />
          <span>Data & History Management</span>
        </h2>
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-xs font-semibold text-white">Clear Evaluation History</h3>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Permanently delete all past resume analysis comparisons while retaining your uploaded resumes.
            </p>
          </div>
          <button
            onClick={() => setShowClearModal(true)}
            className="px-4 py-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 text-xs font-semibold transition-colors whitespace-nowrap self-start sm:self-auto"
          >
            Clear History
          </button>
        </div>
      </div>

      {/* Session Management */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <h2 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <LogOut className="w-4 h-4 text-teal-400" />
          <span>Session Controls</span>
        </h2>
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-xs font-semibold text-white">Sign Out of Current Session</h3>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Securely terminate your JWT authentication session from this browser.
            </p>
          </div>
          <button
            onClick={() => {
              logout();
              navigate('/login');
            }}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors whitespace-nowrap self-start sm:self-auto"
          >
            Sign Out
          </button>
        </div>
      </div>

      {/* Danger Zone: Delete Account */}
      <div className="bg-rose-950/20 border border-rose-900/40 rounded-3xl p-6 shadow-xl space-y-4">
        <h2 className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-2">
          <ShieldAlert className="w-4 h-4" />
          <span>Danger Zone</span>
        </h2>
        <div className="p-4 rounded-2xl bg-slate-950/80 border border-rose-950 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-xs font-semibold text-white">Delete Candidate Account</h3>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Irreversibly delete your profile, all uploaded resumes, and historical analysis records.
            </p>
          </div>
          <button
            onClick={() => setShowDeleteModal(true)}
            className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold shadow-md shadow-rose-600/20 transition-colors whitespace-nowrap self-start sm:self-auto"
          >
            Delete Account
          </button>
        </div>
      </div>

      {/* Clear History Confirmation Modal */}
      {showClearModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 max-w-md w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-amber-400">
                <AlertTriangle className="w-5 h-5" />
                <h3 className="text-sm font-bold text-white">Confirm Clear History</h3>
              </div>
              <button
                onClick={() => setShowClearModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Are you sure you want to clear your complete analysis history? This action cannot be undone.
            </p>
            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setShowClearModal(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold hover:bg-slate-700"
              >
                Cancel
              </button>
              <button
                onClick={handleClearHistory}
                disabled={loading}
                className="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold transition-colors"
              >
                {loading ? 'Clearing...' : 'Yes, Clear All'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Account Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 max-w-md w-full shadow-2xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-rose-400">
                <ShieldAlert className="w-5 h-5" />
                <h3 className="text-sm font-bold text-white">Delete Account Confirmation</h3>
              </div>
              <button
                onClick={() => setShowDeleteModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              This will permanently delete your account, credentials, uploaded PDF files, and analysis history.
              Are you sure you want to proceed?
            </p>
            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold hover:bg-slate-700"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteAccount}
                disabled={loading}
                className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition-colors"
              >
                {loading ? 'Deleting...' : 'Permanently Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
