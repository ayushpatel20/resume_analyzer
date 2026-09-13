import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { LoadingAnalysis } from '../components/LoadingAnalysis';
import {
  Upload,
  FileText,
  X,
  Sparkles,
  AlertCircle,
  Briefcase,
  Layers,
  ArrowRight,
} from 'lucide-react';

export const ResumeAnalysisPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [sampleJDs, setSampleJDs] = useState({});
  const [userResumes, setUserResumes] = useState([]);
  const [selectedResumeId, setSelectedResumeId] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState('');
  const [analyzing, setAnalyzing] = useState(false);

  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  // Load sample JDs and existing resumes on mount
  useEffect(() => {
    const loadData = async () => {
      try {
        const [jdsRes, resumesRes] = await Promise.all([
          api.get('/sample-jds'),
          api.get('/resumes'),
        ]);
        setSampleJDs(jdsRes.data);
        setUserResumes(resumesRes.data);
      } catch (err) {
        console.error('Error loading initial options:', err);
      }
    };
    loadData();
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    validateAndSetFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    validateAndSetFile(file);
  };

  const validateAndSetFile = (file) => {
    setError('');
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Invalid file format. Please upload a PDF resume (.pdf).');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File exceeds 10MB limit. Please upload a smaller PDF file.');
      return;
    }

    setSelectedFile(file);
    setSelectedResumeId(''); // Deselect pre-existing resume
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSelectSampleJD = (roleKey) => {
    const sample = sampleJDs[roleKey];
    if (sample) {
      setJobTitle(sample.title || roleKey);
      setJobDescription(sample.description || '');
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setError('');

    if (!selectedFile && !selectedResumeId) {
      setError('Please upload a PDF resume or select an existing uploaded resume.');
      return;
    }

    if (!jobDescription.trim() || jobDescription.trim().length < 20) {
      setError('Please enter or select a detailed Job Description (at least 20 characters).');
      return;
    }

    setAnalyzing(true);

    try {
      const formData = new FormData();
      if (selectedFile) {
        formData.append('resume_file', selectedFile);
      } else if (selectedResumeId) {
        formData.append('resume_id', selectedResumeId);
      }
      formData.append('job_title', jobTitle.trim() || 'Target Job');
      formData.append('job_description', jobDescription.trim());

      const res = await api.post('/analysis/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Navigate to detailed result page with the new analysis ID
      navigate(`/analysis/${res.data.id}`);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.detail ||
          'Failed to complete analysis. Please ensure the PDF has readable text and try again.'
      );
      setAnalyzing(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return '0 KB';
    const kb = bytes / 1024;
    return kb > 1024 ? `${(kb / 1024).toFixed(1)} MB` : `${kb.toFixed(0)} KB`;
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {analyzing && <LoadingAnalysis />}

      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Resume Analysis & Matching</h1>
        <p className="text-xs text-slate-400 mt-1">
          Upload your resume, specify your target job requirements, and receive comprehensive ATS scores and recommendations.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-start gap-3 text-rose-400 text-xs font-medium">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div className="flex-1 leading-relaxed">{error}</div>
        </div>
      )}

      <form onSubmit={handleAnalyze} className="space-y-6">
        {/* Step 1: Resume Upload / Selection */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-lg bg-teal-500/20 text-teal-400 text-xs font-bold flex items-center justify-center">
                1
              </span>
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Upload or Choose Resume
              </h2>
            </div>
            {userResumes.length > 0 && !selectedFile && (
              <span className="text-[11px] text-slate-400">
                Or pick from {userResumes.length} previous resume(s)
              </span>
            )}
          </div>

          {/* If user has prior resumes, show quick selector */}
          {userResumes.length > 0 && !selectedFile && (
            <div className="mb-4">
              <label className="block text-xs text-slate-400 mb-1 font-medium">
                Use previously uploaded resume:
              </label>
              <select
                value={selectedResumeId}
                onChange={(e) => setSelectedResumeId(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="">-- Or upload a new PDF below --</option>
                {userResumes.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.filename} ({formatFileSize(r.file_size)}) - Uploaded on{' '}
                    {new Date(r.uploaded_at).toLocaleDateString()}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Drag & Drop Area */}
          {!selectedFile ? (
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragOver(true);
              }}
              onDragLeave={() => setIsDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
                isDragOver
                  ? 'border-teal-400 bg-teal-500/10'
                  : 'border-slate-800 hover:border-slate-700 bg-slate-950/40'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={handleFileChange}
              />
              <div className="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center mx-auto mb-3">
                <Upload className="w-6 h-6" />
              </div>
              <p className="text-sm font-semibold text-white">
                Drag and drop your PDF resume here, or <span className="text-teal-400 underline">browse</span>
              </p>
              <p className="text-xs text-slate-500 mt-1">Supports standard text-based PDF files up to 10MB</p>
            </div>
          ) : (
            <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-teal-500/20 border border-teal-500/30 text-teal-300 flex items-center justify-center">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-white truncate max-w-sm">
                    {selectedFile.name}
                  </p>
                  <p className="text-[10px] text-slate-400 mt-0.5">
                    {formatFileSize(selectedFile.size)} &bull; Ready for AI extraction
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={handleRemoveFile}
                className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                title="Remove file"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        {/* Step 2: Job Description */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-lg bg-teal-500/20 text-teal-400 text-xs font-bold flex items-center justify-center">
                2
              </span>
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Target Job Description
              </h2>
            </div>
          </div>

          {/* Sample JD Quick Selectors (Viva & Demo Friendly!) */}
          {Object.keys(sampleJDs).length > 0 && (
            <div className="mb-4">
              <span className="text-[11px] font-semibold text-slate-400 block mb-2 uppercase tracking-wider">
                Quick Demo: Load Sample Job Description
              </span>
              <div className="flex flex-wrap gap-2">
                {Object.keys(sampleJDs).map((role) => (
                  <button
                    key={role}
                    type="button"
                    onClick={() => handleSelectSampleJD(role)}
                    className="px-3 py-1.5 rounded-xl bg-slate-800/90 hover:bg-teal-500/10 border border-slate-700 hover:border-teal-500/40 text-xs text-slate-300 hover:text-teal-300 transition-all font-medium"
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Target Job Title
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <Briefcase className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  value={jobTitle}
                  onChange={(e) => setJobTitle(e.target.value)}
                  placeholder="e.g. Data Scientist / Backend Python Developer"
                  className="block w-full pl-10 pr-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Job Description Requirements & Responsibilities
              </label>
              <textarea
                rows={7}
                required
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the target job description here including required technical skills, tools, responsibilities, and qualifications..."
                className="block w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-teal-500 leading-relaxed transition-colors resize-y"
              />
              <p className="text-[11px] text-slate-500 mt-1.5">
                Tip: Pasting full job descriptions with responsibilities yields more accurate TF-IDF semantic and keyword coverage scores.
              </p>
            </div>
          </div>
        </div>

        {/* Submit Action */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={analyzing || (!selectedFile && !selectedResumeId) || !jobDescription.trim()}
            className="px-8 py-3.5 rounded-2xl bg-gradient-to-r from-teal-500 to-sky-500 text-white font-bold text-sm hover:opacity-95 shadow-xl shadow-teal-500/25 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2.5 transition-all"
          >
            <Sparkles className="w-4 h-4" />
            <span>Analyze Resume Now</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
