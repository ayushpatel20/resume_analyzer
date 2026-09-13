import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { User, Mail, Calendar, Lock, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';

export const ProfilePage = () => {
  const { user, updateUser } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [statusMessage, setStatusMessage] = useState({ type: '', text: '' });
  const [loading, setLoading] = useState(false);

  const handleUpdate = async (e) => {
    e.preventDefault();
    setStatusMessage({ type: '', text: '' });

    if (newPassword && newPassword !== confirmPassword) {
      setStatusMessage({ type: 'error', text: 'New passwords do not match.' });
      return;
    }

    setLoading(true);
    try {
      const payload = { name: name.trim() };
      if (newPassword) {
        payload.current_password = currentPassword;
        payload.new_password = newPassword;
      }
      const res = await api.put('/auth/profile', payload);
      updateUser(res.data);
      setStatusMessage({ type: 'success', text: 'Profile updated successfully!' });
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      setStatusMessage({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to update profile.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Candidate Profile</h1>
        <p className="text-xs text-slate-400 mt-1">Manage your account information and security credentials.</p>
      </div>

      {statusMessage.text && (
        <div
          className={`p-4 rounded-2xl flex items-center gap-2.5 text-xs font-medium border ${
            statusMessage.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300'
              : 'bg-rose-500/10 border-rose-500/20 text-rose-300'
          }`}
        >
          {statusMessage.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-emerald-400" />
          ) : (
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
          )}
          <span>{statusMessage.text}</span>
        </div>
      )}

      {/* Account Info Summary Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <h2 className="text-xs font-bold text-white uppercase tracking-wider">Account Overview</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800/80 flex items-center gap-3">
            <Mail className="w-4 h-4 text-teal-400 flex-shrink-0" />
            <div>
              <span className="text-[10px] text-slate-500 uppercase font-semibold block">Email</span>
              <span className="text-slate-200 font-medium truncate block">{user?.email}</span>
            </div>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800/80 flex items-center gap-3">
            <Calendar className="w-4 h-4 text-sky-400 flex-shrink-0" />
            <div>
              <span className="text-[10px] text-slate-500 uppercase font-semibold block">Joined Date</span>
              <span className="text-slate-200 font-medium">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Active'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Edit Profile Form */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        <h2 className="text-xs font-bold text-white uppercase tracking-wider mb-4">Edit Profile & Password</h2>
        <form onSubmit={handleUpdate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Full Name
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                <User className="w-4 h-4" />
              </div>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="block w-full pl-10 pr-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-500"
              />
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800/80">
            <h3 className="text-xs font-semibold text-slate-400 mb-3">Change Password (Optional)</h3>
            <div className="space-y-3">
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Current Password</label>
                <input
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Leave blank to keep unchanged"
                  className="block w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                />
              </div>

              <div>
                <label className="block text-[11px] text-slate-400 mb-1">New Password</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  className="block w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                />
              </div>

              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Confirm New Password</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Re-type new password"
                  className="block w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-3">
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white text-xs font-bold hover:opacity-95 shadow-md shadow-teal-500/20 disabled:opacity-50 flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
