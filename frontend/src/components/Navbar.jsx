import React from 'react';
import { Menu, Bell, Sparkles, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export const Navbar = ({ setIsSidebarOpen }) => {
  const { user } = useAuth();

  return (
    <header className="h-16 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80 sticky top-0 z-30 px-4 sm:px-6 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          onClick={() => setIsSidebarOpen((prev) => !prev)}
          className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-900 lg:hidden"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-2">
          <span className="hidden sm:inline-block px-2.5 py-1 rounded-full text-[10px] font-semibold tracking-wider uppercase bg-teal-500/10 text-teal-400 border border-teal-500/20">
            B.Tech Mini Project 2026
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Link
          to="/analyze"
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-white text-xs font-semibold hover:opacity-95 shadow-md shadow-teal-500/20 transition-all"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>New Analysis</span>
        </Link>

        <Link
          to="/profile"
          className="flex items-center gap-2 pl-2 pr-3 py-1 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors"
        >
          <div className="w-6 h-6 rounded-lg bg-teal-500/20 text-teal-300 flex items-center justify-center text-xs font-bold">
            {user?.name?.charAt(0) || 'U'}
          </div>
          <span className="text-xs font-medium text-slate-200 hidden md:inline-block">
            {user?.name || 'Account'}
          </span>
        </Link>
      </div>
    </header>
  );
};
