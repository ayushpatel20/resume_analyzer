import React, { useState, useEffect } from 'react';
import { Sparkles, CheckCircle2, Circle } from 'lucide-react';

const STEPS = [
  'Reading resume & validating document structure...',
  'Extracting personal details & contact credentials...',
  'Scanning and extracting technical skills...',
  'Vectorizing text & computing TF-IDF Cosine Similarity...',
  'Comparing candidate proficiencies with Job Description...',
  'Evaluating resume section depth & quality score...',
  'Ranking best-fit career profiles & generating ethical suggestions...',
];

export const LoadingAnalysis = () => {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 700);

    return () => clearInterval(interval);
  }, []);

  const progressPercent = Math.round(((activeStep + 1) / STEPS.length) * 100);

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 max-w-md w-full shadow-2xl relative overflow-hidden">
        {/* Glow effect */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-48 h-2 bg-gradient-to-r from-teal-500 to-sky-500 rounded-full blur-sm" />

        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-teal-500/10 border border-teal-500/20 rounded-2xl">
            <Sparkles className="w-6 h-6 text-teal-400 animate-pulse" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Analyzing Resume</h3>
            <p className="text-xs text-slate-400">Running AI / NLP Evaluation Pipeline</p>
          </div>
        </div>

        {/* Progress bar */}
        <div className="mb-6">
          <div className="flex justify-between text-xs font-semibold text-slate-400 mb-2">
            <span>Processing Pipeline</span>
            <span className="text-teal-400">{progressPercent}%</span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-teal-500 to-sky-500 h-full rounded-full transition-all duration-500 ease-out"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Animated steps */}
        <div className="space-y-3">
          {STEPS.map((step, idx) => {
            const isCompleted = idx < activeStep;
            const isCurrent = idx === activeStep;
            const isPending = idx > activeStep;

            return (
              <div
                key={idx}
                className={`flex items-center gap-3 text-xs transition-opacity duration-300 ${
                  isPending ? 'opacity-30' : 'opacity-100'
                }`}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-4 h-4 text-teal-400 flex-shrink-0" />
                ) : isCurrent ? (
                  <div className="w-4 h-4 rounded-full border-2 border-teal-400 border-t-transparent animate-spin flex-shrink-0" />
                ) : (
                  <Circle className="w-4 h-4 text-slate-600 flex-shrink-0" />
                )}
                <span
                  className={`${
                    isCurrent
                      ? 'text-white font-medium'
                      : isCompleted
                      ? 'text-slate-400'
                      : 'text-slate-600'
                  }`}
                >
                  {step}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
