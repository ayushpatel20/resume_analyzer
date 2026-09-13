import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  FileCheck2,
  Cpu,
  Target,
  ArrowRight,
  ShieldCheck,
  Zap,
  BarChart3,
  Award,
  ChevronRight,
  Database,
  Code2,
} from 'lucide-react';

export const LandingPage = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-teal-500 selection:text-white">
      {/* Top Navigation */}
      <header className="border-b border-slate-800/80 sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-500 to-sky-500 flex items-center justify-center shadow-lg shadow-teal-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-bold text-lg text-white tracking-tight">ResumeAI</span>
              <span className="hidden sm:inline-block ml-2 text-[10px] px-2 py-0.5 rounded-full bg-teal-500/10 text-teal-400 border border-teal-500/20 font-semibold uppercase tracking-wider">
                B.Tech Mini Project
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="text-sm font-medium text-slate-300 hover:text-white transition-colors px-3 py-1.5"
            >
              Sign In
            </Link>
            <Link
              to="/signup"
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white text-xs font-semibold hover:opacity-95 shadow-lg shadow-teal-500/20 transition-all"
            >
              <span>Get Started</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-24 px-6 overflow-hidden">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs text-teal-400 font-medium mb-6">
            <Zap className="w-3.5 h-3.5" />
            <span>Automated ATS Compatibility & Skill Gap Engine</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight sm:leading-none mb-6">
            AI Resume Analyzer &{' '}
            <span className="bg-gradient-to-r from-teal-400 via-sky-400 to-indigo-400 bg-clip-text text-transparent">
              Job Matching System
            </span>
          </h1>

          <p className="text-base sm:text-xl text-slate-400 max-w-2xl mx-auto font-normal leading-relaxed mb-10">
            Analyze your resume against real-world Job Descriptions. Discover missing skills,
            compute transparent ATS scores, and receive ethical recommendations to land your dream job.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/signup"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white font-semibold text-sm hover:opacity-95 shadow-xl shadow-teal-500/25 flex items-center justify-center gap-2 transition-all"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/login"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white font-semibold text-sm hover:border-slate-700 transition-all flex items-center justify-center"
            >
              Sign In to Dashboard
            </Link>
          </div>

          {/* Quick trust metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-16 pt-12 border-t border-slate-800/80">
            <div>
              <div className="text-2xl font-bold text-white">TF-IDF</div>
              <div className="text-xs text-slate-400 mt-0.5">Cosine Similarity</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-teal-400">100+</div>
              <div className="text-xs text-slate-400 mt-0.5">Categorized Skills</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-sky-400">0-100</div>
              <div className="text-xs text-slate-400 mt-0.5">Resume Quality Rubric</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-indigo-400">ReportLab</div>
              <div className="text-xs text-slate-400 mt-0.5">PDF Report Export</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-6 bg-slate-900/50 border-y border-slate-800/80">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-teal-400 mb-2">
              Step-by-Step Workflow
            </h2>
            <p className="text-3xl font-bold text-white">How the System Evaluates Resumes</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              {
                step: '01',
                title: 'Upload PDF Resume',
                desc: 'Upload any standard text-based PDF resume. Text is safely extracted using PyMuPDF.',
                icon: FileCheck2,
              },
              {
                step: '02',
                title: 'Paste Job Description',
                desc: 'Provide your target job requirements or pick from preloaded industry descriptions.',
                icon: Target,
              },
              {
                step: '03',
                title: 'Run AI Matching Pipeline',
                desc: 'Calculates TF-IDF vector similarity, extracts domain skills, and detects missing keywords.',
                icon: Cpu,
              },
              {
                step: '04',
                title: 'Export Evaluation Report',
                desc: 'Download a clean, viva-ready PDF report summarizing scores, fit percentages, and tips.',
                icon: Award,
              },
            ].map((item, idx) => {
              const Icon = item.icon;
              return (
                <div
                  key={idx}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-6 relative group hover:border-slate-700 transition-all"
                >
                  <div className="text-3xl font-black text-slate-800 group-hover:text-teal-500/20 transition-colors mb-4">
                    {item.step}
                  </div>
                  <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 mb-4">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="text-base font-semibold text-white mb-2">{item.title}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{item.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-sky-400 mb-2">
              Comprehensive Features
            </h2>
            <p className="text-3xl font-bold text-white">Engineered for Academic & Industry Rigor</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                title: 'Transparent ATS Scoring',
                desc: 'Formula-backed score combining 50% TF-IDF Cosine Similarity, 30% Skill Coverage, and 20% Keyword Match.',
                icon: BarChart3,
              },
              {
                title: '0-100 Quality Rubric',
                desc: 'Evaluates structural completeness across Contact, Summary, Education, Skills, Projects, Experience, and Metrics.',
                icon: Zap,
              },
              {
                title: 'Skill Gap Identification',
                desc: 'Highlights matched technologies and lists missing skills with ethical, genuine suggestions.',
                icon: Target,
              },
              {
                title: 'Job Role Recommendations',
                desc: 'Matches detected profile skills against curated roles (Data Analyst, ML Engineer, Python Dev, etc.).',
                icon: Award,
              },
              {
                title: 'Section Detection Engine',
                desc: 'Rule-based regex scanner verifying presence of all essential academic and industry sections.',
                icon: ShieldCheck,
              },
              {
                title: 'ReportLab PDF Generation',
                desc: 'Produces publication-grade downloadable evaluation summaries on demand.',
                icon: FileCheck2,
              },
            ].map((f, idx) => {
              const Icon = f.icon;
              return (
                <div
                  key={idx}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-slate-700 transition-all"
                >
                  <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-teal-400 mb-4">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="text-base font-semibold text-white mb-2">{f.title}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{f.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology & Viva Section */}
      <section className="py-16 px-6 bg-slate-900/30 border-t border-slate-800/80">
        <div className="max-w-5xl mx-auto bg-slate-900 border border-slate-800 rounded-3xl p-8 sm:p-12 relative overflow-hidden">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/10 text-teal-400 text-xs font-semibold mb-4">
                <Code2 className="w-3.5 h-3.5" />
                <span>Viva-Friendly Architecture</span>
              </div>
              <h3 className="text-2xl sm:text-3xl font-bold text-white mb-3">
                Built with Pure Open-Source AI/NLP
              </h3>
              <p className="text-sm text-slate-400 max-w-xl leading-relaxed">
                No black-box third-party paid APIs. The system employs scikit-learn, TF-IDF vectorization,
                regex token boundaries, FastAPI REST APIs, and ReportLab PDF compilation, making every
                algorithmic decision easily explainable during viva voce examinations.
              </p>
            </div>
            <Link
              to="/signup"
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white text-xs font-semibold hover:opacity-95 shadow-lg shadow-teal-500/20 whitespace-nowrap"
            >
              Test Project Now
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-10 px-6 text-center text-xs text-slate-500">
        <p className="mb-2">
          AI Resume Analyzer and Job Matching System &bull; 7th Semester B.Tech Mini Project 2026
        </p>
        <p className="text-[11px] text-slate-600">
          Designed with React, Tailwind CSS, FastAPI, SQLAlchemy, and Scikit-learn.
        </p>
      </footer>
    </div>
  );
};
