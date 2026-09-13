import React from 'react';

export const ScoreCard = ({ title, score, max = 100, subtitle, icon: Icon, color = 'teal', size = 'normal' }) => {
  const numScore = Number(score || 0);
  const percentage = Math.min(100, Math.max(0, (numScore / max) * 100));

  // Determine badge color based on performance
  let colorClasses = {
    ring: 'text-teal-400 stroke-teal-500',
    bg: 'bg-teal-500/10 text-teal-400 border-teal-500/20',
    accent: 'from-teal-500 to-emerald-500',
  };

  if (color === 'blue') {
    colorClasses = {
      ring: 'text-sky-400 stroke-sky-500',
      bg: 'bg-sky-500/10 text-sky-400 border-sky-500/20',
      accent: 'from-sky-500 to-indigo-500',
    };
  } else if (color === 'amber') {
    colorClasses = {
      ring: 'text-amber-400 stroke-amber-500',
      bg: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
      accent: 'from-amber-500 to-orange-500',
    };
  } else if (color === 'purple') {
    colorClasses = {
      ring: 'text-purple-400 stroke-purple-500',
      bg: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
      accent: 'from-purple-500 to-pink-500',
    };
  }

  // Calculate circular SVG progress
  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all duration-200 shadow-xl relative overflow-hidden group">
      {/* Subtle background glow */}
      <div className={`absolute -right-8 -top-8 w-24 h-24 bg-gradient-to-br ${colorClasses.accent} opacity-5 rounded-full blur-2xl group-hover:opacity-10 transition-opacity`} />

      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            {Icon && <Icon className="w-4 h-4 text-slate-400" />}
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-extrabold text-white tracking-tight">{numScore.toFixed(0)}</span>
            <span className="text-sm font-medium text-slate-500">/{max}%</span>
          </div>
          {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
        </div>

        {/* Circular Progress Gauge */}
        <div className="relative w-20 h-20 flex items-center justify-center flex-shrink-0">
          <svg className="w-20 h-20 transform -rotate-90">
            <circle
              cx="40"
              cy="40"
              r={radius}
              className="text-slate-800"
              strokeWidth="6"
              stroke="currentColor"
              fill="transparent"
            />
            <circle
              cx="40"
              cy="40"
              r={radius}
              className={colorClasses.ring}
              strokeWidth="6"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              stroke="currentColor"
              fill="transparent"
              style={{ transition: 'stroke-dashoffset 0.8s ease-in-out' }}
            />
          </svg>
          <span className="absolute text-xs font-bold text-slate-300">{Math.round(percentage)}%</span>
        </div>
      </div>
    </div>
  );
};
