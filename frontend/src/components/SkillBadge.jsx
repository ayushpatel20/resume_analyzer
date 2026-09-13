import React from 'react';
import { Check, Plus, Tag } from 'lucide-react';

export const SkillBadge = ({ skill, status = 'detected', category }) => {
  let badgeStyles = 'bg-slate-800 text-slate-300 border-slate-700';
  let Icon = Tag;

  if (status === 'matched') {
    badgeStyles = 'bg-emerald-950/60 text-emerald-300 border-emerald-500/30';
    Icon = Check;
  } else if (status === 'missing') {
    badgeStyles = 'bg-rose-950/60 text-rose-300 border-rose-500/30';
    Icon = Plus;
  } else if (status === 'detected') {
    badgeStyles = 'bg-sky-950/60 text-sky-300 border-sky-500/30';
    Icon = Tag;
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium border ${badgeStyles} transition-colors shadow-sm`}>
      <Icon className="w-3.5 h-3.5 flex-shrink-0" />
      <span>{typeof skill === 'string' ? skill : skill.name || skill.skill_name}</span>
      {category && (
        <span className="text-[10px] opacity-60 ml-0.5 uppercase tracking-wider font-semibold">
          · {category}
        </span>
      )}
    </span>
  );
};
