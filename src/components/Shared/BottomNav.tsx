import React from 'react';
import { LayoutDashboard, BarChart3, Wallet, Settings } from 'lucide-react';
import { Screen } from '../../types';

export const BottomNav = ({ current, onNavigate }: { current: Screen, onNavigate: (s: Screen) => void }) => (
  <nav className="fixed bottom-8 left-1/2 -translate-x-1/2 w-[280px] h-16 bg-background-dark/95 backdrop-blur-xl border border-white/10 rounded-full flex items-center justify-around px-2 shadow-2xl z-50">
    <button 
      onClick={() => onNavigate('dashboard')}
      className={`flex items-center justify-center w-12 h-12 rounded-full transition-colors ${current === 'dashboard' ? 'bg-primary text-background-dark' : 'text-slate-400 hover:text-white'}`}
    >
      <LayoutDashboard className="w-6 h-6" />
    </button>
    <button 
      onClick={() => onNavigate('analysis')}
      className={`flex items-center justify-center w-12 h-12 rounded-full transition-colors ${current === 'analysis' ? 'bg-primary text-background-dark' : 'text-slate-400 hover:text-white'}`}
    >
      <BarChart3 className="w-6 h-6" />
    </button>
    <button 
      onClick={() => onNavigate('upload')}
      className={`flex items-center justify-center w-12 h-12 rounded-full transition-colors ${current === 'upload' ? 'bg-primary text-background-dark' : 'text-slate-400 hover:text-white'}`}
    >
      <Wallet className="w-6 h-6" />
    </button>
    <button 
      className="flex items-center justify-center w-12 h-12 rounded-full text-slate-400 hover:text-white transition-colors"
    >
      <Settings className="w-6 h-6" />
    </button>
  </nav>
);
