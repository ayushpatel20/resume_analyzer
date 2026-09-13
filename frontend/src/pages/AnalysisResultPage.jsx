import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ScoreCard } from '../components/ScoreCard';
import { SkillBadge } from '../components/SkillBadge';
import {
  Download,
  FileText,
  User,
  Mail,
  Phone,
  GraduationCap,
  Link2,
  Code2,
  CheckCircle2,
  XCircle,
  TrendingUp,
  AlertCircle,
  Lightbulb,
  Briefcase,
  ChevronLeft,
  Sparkles,
  Info,
  Layers,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

export const AnalysisResultPage = () => {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [downloading, setDownloading] = useState(false);
  const [activeSkillTab, setActiveSkillTab] = useState('matched');

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const res = await api.get(`/analysis/${id}`);
        setAnalysis(res.data);
      } catch (err) {
        console.error('Error fetching analysis details:', err);
        setError('Failed to load analysis record. It may not exist or belongs to another user.');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, [id]);

  const handleDownloadReport = async () => {
    setDownloading(true);
    try {
      const response = await api.get(`/reports/${id}`, {
        responseType: 'blob',
      });
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Resume_Analysis_Report_${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download error:', err);
      alert('Unable to generate PDF report at this time. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-slate-400">
        <Sparkles className="w-8 h-8 text-teal-400 animate-spin mx-auto mb-3" />
        <p className="text-sm font-semibold text-white">Loading evaluation results...</p>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center">
        <AlertCircle className="w-12 h-12 text-rose-400 mx-auto mb-4" />
        <h2 className="text-xl font-bold text-white mb-2">Analysis Not Found</h2>
        <p className="text-xs text-slate-400 mb-6">{error || 'Unable to retrieve analysis details.'}</p>
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 text-slate-200 text-xs font-semibold hover:bg-slate-700"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Return to Dashboard</span>
        </Link>
      </div>
    );
  }

  const matchedSkills = analysis.skills.filter((s) => s.status === 'matched');
  const missingSkills = analysis.skills.filter((s) => s.status === 'missing');
  const detectedSkills = analysis.skills.filter((s) => s.status === 'detected' || s.status === 'matched');

  // Prepare chart data for Resume Quality Rubric
  const rubricData = analysis.score_breakdown?.resume_rubric
    ? Object.entries(analysis.score_breakdown.resume_rubric).map(([key, val]) => ({
        name: key.length > 14 ? key.substring(0, 14) + '...' : key,
        score: val.score,
        max: val.max,
      }))
    : [];

  // Prepare chart data for Role Recommendations
  const roleChartData = (analysis.recommendations || []).map((r) => ({
    name: r.job_role,
    matchScore: r.score,
  }));

  const info = analysis.extracted_info || {};
  const sections = analysis.detected_sections || {};

  return (
    <div className="space-y-8">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Link
              to="/dashboard"
              className="text-slate-400 hover:text-white transition-colors p-1 -ml-1 rounded-lg"
            >
              <ChevronLeft className="w-4 h-4" />
            </Link>
            <span className="text-xs font-semibold uppercase tracking-wider text-teal-400">
              Evaluation Completed
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Analysis: {analysis.job_title}
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            File: <span className="text-slate-200 font-medium">{analysis.resume_filename}</span> &bull;
            Evaluated on {new Date(analysis.created_at).toLocaleDateString()} at{' '}
            {new Date(analysis.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>

        <button
          onClick={handleDownloadReport}
          disabled={downloading}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white text-xs font-bold hover:opacity-95 shadow-lg shadow-teal-500/20 disabled:opacity-50 transition-all self-start sm:self-auto"
        >
          <Download className="w-4 h-4" />
          <span>{downloading ? 'Generating PDF...' : 'Download PDF Report'}</span>
        </button>
      </div>

      {/* Top 4 Score Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <ScoreCard
          title="ATS Compatibility"
          score={analysis.ats_score}
          subtitle="Weighted Algorithm Match"
          icon={TrendingUp}
          color="teal"
        />
        <ScoreCard
          title="Resume Quality"
          score={analysis.resume_score}
          subtitle="Structure & Depth Rubric"
          icon={CheckCircle2}
          color="blue"
        />
        <ScoreCard
          title="Skill Match"
          score={analysis.skill_match_score}
          subtitle={`${matchedSkills.length} Matched / ${matchedSkills.length + missingSkills.length} Required`}
          icon={Layers}
          color="amber"
        />
        <ScoreCard
          title="Keyword Match"
          score={analysis.keyword_score}
          subtitle="Frequency & Coverage Ratio"
          icon={FileText}
          color="purple"
        />
      </div>

      {/* Viva / Algorithm Explainer Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg relative overflow-hidden">
        <div className="flex items-start gap-3">
          <div className="p-2 bg-teal-500/10 border border-teal-500/20 rounded-xl text-teal-400 mt-0.5">
            <Info className="w-4 h-4" />
          </div>
          <div className="flex-1">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">
              ATS-Style Compatibility Score Formula Breakdown (Viva Reference)
            </h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              ATS Score = <strong className="text-teal-300">50% Semantic Similarity</strong> (TF-IDF Cosine:{' '}
              {analysis.semantic_score}%) + <strong className="text-sky-300">30% Skill Coverage</strong> ({analysis.skill_match_score}%) +{' '}
              <strong className="text-amber-300">20% Keyword Match</strong> ({analysis.keyword_score}%).
            </p>
          </div>
        </div>
      </div>

      {/* Two Column Layout: Extracted Info & Section Checklist */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Candidate Information Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl lg:col-span-1">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
            <User className="w-4 h-4 text-teal-400" />
            <span>Extracted Credentials</span>
          </h2>

          <div className="space-y-3.5 text-xs">
            <div className="flex items-start gap-3">
              <User className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">Name</span>
                <span className="text-slate-100 font-medium">{info.name || 'Not detected'}</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Mail className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">Email</span>
                <span className="text-slate-100 font-medium truncate">{info.email || 'Not detected'}</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Phone className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">Phone</span>
                <span className="text-slate-100 font-medium">{info.phone || 'Not detected'}</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <GraduationCap className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">Degree / Education</span>
                <span className="text-slate-100 font-medium">{info.degree || 'Not detected'}</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Link2 className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">LinkedIn</span>
                {info.linkedin && info.linkedin !== 'Not detected' ? (
                  <a
                    href={info.linkedin}
                    target="_blank"
                    rel="noreferrer"
                    className="text-teal-400 hover:underline truncate block max-w-[200px]"
                  >
                    {info.linkedin}
                  </a>
                ) : (
                  <span className="text-slate-500">Not detected</span>
                )}
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Code2 className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">GitHub</span>
                {info.github && info.github !== 'Not detected' ? (
                  <a
                    href={info.github}
                    target="_blank"
                    rel="noreferrer"
                    className="text-teal-400 hover:underline truncate block max-w-[200px]"
                  >
                    {info.github}
                  </a>
                ) : (
                  <span className="text-slate-500">Not detected</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Section Verification Checklist */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl lg:col-span-2">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-teal-400" />
            <span>Resume Section Verification</span>
          </h2>
          <p className="text-xs text-slate-400 mb-4">
            Standard ATS parsers search for established section headings to categorize your career history.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
            {Object.entries(sections).map(([sec, present]) => (
              <div
                key={sec}
                className={`p-3 rounded-2xl border flex items-center gap-2.5 ${
                  present
                    ? 'bg-emerald-950/20 border-emerald-500/20 text-emerald-300'
                    : 'bg-slate-950/50 border-slate-800 text-slate-500'
                }`}
              >
                {present ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                ) : (
                  <XCircle className="w-4 h-4 text-slate-600 flex-shrink-0" />
                )}
                <span className={`font-semibold ${present ? 'text-white' : 'text-slate-400'}`}>
                  {sec}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Skills Analysis Section with Tabs */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Layers className="w-4 h-4 text-teal-400" />
              <span>Skills Evaluation & Gap Detection</span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Comparison between candidate skills and required technical skills specified in Job Description.
            </p>
          </div>

          <div className="flex p-1 bg-slate-950 border border-slate-800 rounded-xl">
            <button
              onClick={() => setActiveSkillTab('matched')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeSkillTab === 'matched'
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Matched ({matchedSkills.length})
            </button>
            <button
              onClick={() => setActiveSkillTab('missing')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeSkillTab === 'missing'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Missing Gaps ({missingSkills.length})
            </button>
            <button
              onClick={() => setActiveSkillTab('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeSkillTab === 'all'
                  ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              All Detected ({detectedSkills.length})
            </button>
          </div>
        </div>

        {activeSkillTab === 'matched' && (
          <div>
            {matchedSkills.length === 0 ? (
              <p className="text-xs text-slate-500 py-4">No explicit skill matches detected in target JD.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {matchedSkills.map((s) => (
                  <SkillBadge key={s.id} skill={s.skill_name} status="matched" />
                ))}
              </div>
            )}
          </div>
        )}

        {activeSkillTab === 'missing' && (
          <div>
            <div className="mb-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs flex items-center gap-2">
              <Lightbulb className="w-4 h-4 flex-shrink-0 text-amber-400" />
              <span>
                <strong>Ethical Note:</strong> Consider adding these skills to your resume only if you genuinely have project or professional experience with them.
              </span>
            </div>
            {missingSkills.length === 0 ? (
              <p className="text-xs text-emerald-400 py-4 font-semibold">
                Outstanding! No tracked required skills from the job description are missing in your resume.
              </p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {missingSkills.map((s) => (
                  <SkillBadge key={s.id} skill={s.skill_name} status="missing" />
                ))}
              </div>
            )}
          </div>
        )}

        {activeSkillTab === 'all' && (
          <div className="flex flex-wrap gap-2">
            {detectedSkills.map((s) => (
              <SkillBadge key={s.id} skill={s.skill_name} status="detected" />
            ))}
          </div>
        )}
      </div>

      {/* Visual Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Resume Quality Rubric Breakdown Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-2 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-sky-400" />
            <span>Resume Quality Score Breakdown</span>
          </h2>
          <p className="text-xs text-slate-400 mb-6">
            Detailed scoring across 9 professional content and layout dimensions (0-100).
          </p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rubricData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 9 }} interval={0} angle={-25} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={[0, 15]} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px' }}
                  itemStyle={{ color: '#38bdf8' }}
                />
                <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                  {rubricData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.score >= entry.max * 0.7 ? '#0284c7' : '#f59e0b'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Job Role Recommendation Compatibility Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-2 flex items-center gap-2">
            <Briefcase className="w-4 h-4 text-teal-400" />
            <span>Top Recommended Career Roles</span>
          </h2>
          <p className="text-xs text-slate-400 mb-6">
            Fit compatibility scores calculated from your detected skillset across curated roles.
          </p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={roleChartData} layout="vertical" margin={{ top: 10, right: 20, left: 40, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" tick={{ fontSize: 10 }} width={90} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px' }}
                  itemStyle={{ color: '#14b8a6' }}
                />
                <Bar dataKey="matchScore" fill="#0d9488" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recommended Job Profiles Detail Cards */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
          <Briefcase className="w-4 h-4 text-teal-400" />
          <span>Role Recommendation Explanations</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {(analysis.recommendations || []).slice(0, 4).map((rec, idx) => (
            <div key={idx} className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xs font-bold text-white">{rec.job_role}</h3>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-teal-500/10 text-teal-300 border border-teal-500/20">
                  {rec.score.toFixed(0)}% Fit
                </span>
              </div>
              <div className="text-[11px] space-y-1 text-slate-400">
                <p>
                  <strong className="text-slate-300">Matched:</strong>{' '}
                  {rec.matched_skills?.length > 0 ? rec.matched_skills.join(', ') : 'None'}
                </p>
                <p>
                  <strong className="text-slate-300">Gaps to Learn:</strong>{' '}
                  {rec.missing_skills?.length > 0 ? rec.missing_skills.slice(0, 5).join(', ') : 'None'}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Resume Improvement Suggestions */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-2 flex items-center gap-2">
          <Lightbulb className="w-4 h-4 text-amber-400" />
          <span>Actionable Improvement Engine</span>
        </h2>
        <p className="text-xs text-slate-400 mb-6">
          Constructive, rule-based suggestions to optimize your resume impact without fabricating qualifications.
        </p>

        <div className="space-y-3">
          {(analysis.suggestions || []).map((sugg, idx) => (
            <div
              key={idx}
              className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 flex items-start gap-3.5 text-xs leading-relaxed"
            >
              <div className="w-6 h-6 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 mt-0.5 font-bold text-[10px]">
                {idx + 1}
              </div>
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5">
                  [{sugg.category}]
                </span>
                <p className="text-slate-200">{sugg.suggestion}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
