import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { ScoreCard } from '../components/ScoreCard';
import {
  FileSearch,
  Sparkles,
  Files,
  ArrowUpRight,
  TrendingUp,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Layers,
  FileText,
} from 'lucide-react';

export const DashboardPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/analysis/dashboard-stats');
        setStats(res.data);
      } catch (err) {
        console.error('Error fetching dashboard statistics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden bg-gradient-to-r from-slate-900 via-slate-900 to-teal-950/40 border border-slate-800 rounded-3xl p-6 sm:p-8">
        <div className="max-w-2xl relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Resume Intelligence Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Welcome back, {user?.name || 'Candidate'}!
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-2 leading-relaxed">
            Ready to optimize your resume for your target dream role? Upload your resume, compare against job descriptions,
            and inspect ATS compatibility scores in seconds.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white text-xs font-semibold hover:opacity-95 shadow-lg shadow-teal-500/20 transition-all"
            >
              <FileSearch className="w-4 h-4" />
              <span>Start New Analysis</span>
            </Link>
            <Link
              to="/resumes"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-slate-300 hover:text-white text-xs font-semibold hover:bg-slate-800 transition-all"
            >
              <Files className="w-4 h-4" />
              <span>Manage Resumes</span>
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <ScoreCard
          title="Latest ATS Match"
          score={stats?.latest_ats_score || 0}
          subtitle="Compatibility with Target JD"
          icon={TrendingUp}
          color="teal"
        />
        <ScoreCard
          title="Resume Quality"
          score={stats?.latest_resume_score || 0}
          subtitle="Structural & Content Rubric"
          icon={CheckCircle2}
          color="blue"
        />
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Layers className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Skills Detected
              </span>
            </div>
            <div className="text-3xl font-extrabold text-white">
              {stats?.total_skills_detected || 0}
            </div>
            <p className="text-xs text-slate-400 mt-1">Identified across domains</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <CheckCircle2 className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <AlertTriangle className="w-4 h-4 text-rose-400" />
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Missing Skills
              </span>
            </div>
            <div className="text-3xl font-extrabold text-white">
              {stats?.total_missing_skills || 0}
            </div>
            <p className="text-xs text-slate-400 mt-1">Gaps in target role</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
            <AlertTriangle className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Recent Analyses Section */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">Recent Analyses</h2>
            <p className="text-xs text-slate-400">Your latest resume evaluations and compatibility reports</p>
          </div>
          <Link
            to="/history"
            className="text-xs font-semibold text-teal-400 hover:text-teal-300 flex items-center gap-1"
          >
            <span>View All</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-12 text-slate-500 text-xs">Loading recent analyses...</div>
        ) : stats?.recent_analyses?.length === 0 ? (
          <div className="text-center py-12 border border-dashed border-slate-800 rounded-2xl">
            <FileText className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-sm font-semibold text-slate-300">No analyses generated yet</p>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-4">
              Upload your first resume and compare it with a target job description to see detailed scores and skill gaps.
            </p>
            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-semibold hover:bg-teal-500/20 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Run First Analysis</span>
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800/80 uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="pb-3 pl-2">Resume File</th>
                  <th className="pb-3">Target Job Title</th>
                  <th className="pb-3 text-center">ATS Score</th>
                  <th className="pb-3 text-center">Quality Score</th>
                  <th className="pb-3">Date</th>
                  <th className="pb-3 text-right pr-2">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {stats.recent_analyses.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 pl-2 font-medium text-white flex items-center gap-2">
                      <FileText className="w-4 h-4 text-teal-400 flex-shrink-0" />
                      <span className="truncate max-w-[180px]">{item.resume_filename}</span>
                    </td>
                    <td className="py-3.5 text-slate-300 font-medium">
                      {item.job_title}
                    </td>
                    <td className="py-3.5 text-center">
                      <span className="inline-block px-2.5 py-1 rounded-full text-xs font-bold bg-teal-500/10 text-teal-400 border border-teal-500/20">
                        {item.ats_score.toFixed(0)}%
                      </span>
                    </td>
                    <td className="py-3.5 text-center">
                      <span className="inline-block px-2.5 py-1 rounded-full text-xs font-bold bg-sky-500/10 text-sky-400 border border-sky-500/20">
                        {item.resume_score.toFixed(0)}/100
                      </span>
                    </td>
                    <td className="py-3.5 text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-slate-500" />
                        <span>{new Date(item.created_at).toLocaleDateString()}</span>
                      </div>
                    </td>
                    <td className="py-3.5 text-right pr-2">
                      <Link
                        to={`/analysis/${item.id}`}
                        className="inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors"
                      >
                        <span>View</span>
                        <ArrowUpRight className="w-3 h-3" />
                      </Link>
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
