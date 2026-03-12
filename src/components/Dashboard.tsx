import React from 'react';
import { motion } from 'motion/react';
import { ArrowRight, Zap, Landmark, LayoutDashboard, BarChart3, Plus, Upload as UploadIcon, History } from 'lucide-react';
import { Screen, ActivityItem } from '../types';

export const Dashboard = ({ onNavigate }: { onNavigate: (s: Screen) => void }) => {
  const activities: ActivityItem[] = [
    { id: '1', name: 'Olymax Systems, Pvt. Ltd.', time: '2 hours ago', status: 'approved', icon: 'business' },
    { id: '2', name: 'Assam Carbon Products Ltd.', time: '5 hours ago', status: 'processing', icon: 'store' },
    { id: '3', name: 'Stayzilla', time: 'Yesterday', status: 'rejected', icon: 'rocket' },
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="max-w-4xl mx-auto px-6 pb-32"
    >
      <div className="mb-8">
        <h2 className="text-4xl font-black tracking-tight mb-1">Hi there..</h2>
        <p className="text-slate-500 font-medium">Ready for today's analysis?</p>
      </div>

      <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-primary via-[#82d62d] to-[#69b321] p-8 shadow-2xl shadow-primary/20 mb-10">
        <div className="absolute -right-12 -top-12 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
        <div className="absolute -left-12 -bottom-12 w-48 h-48 bg-black/10 rounded-full blur-2xl"></div>
        <div className="relative z-10 backdrop-blur-md bg-white/10 border border-white/20 rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <p className="text-background-dark/70 font-bold uppercase tracking-wider text-xs mb-1">Portfolio Snapshot</p>
            <h3 className="text-background-dark text-4xl font-black mb-1">24 Active Appraisals</h3>
          </div>
          <button 
            onClick={() => onNavigate('analysis')}
            className="bg-background-dark text-primary px-6 py-3 rounded-full font-bold text-sm flex items-center gap-2 self-start md:self-center transition-transform active:scale-95"
          >
            View Details
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <section className="mb-10">
        <h4 className="text-slate-900 font-bold mb-5 flex items-center gap-2">
          <Zap className="w-5 h-5 text-primary fill-primary" /> Quick Actions
        </h4>
        <div className="grid grid-cols-3 gap-4">
          <button onClick={() => onNavigate('onboarding')} className="flex flex-col items-center gap-3 group">
            <div className="w-20 h-20 rounded-full bg-primary flex items-center justify-center text-background-dark shadow-lg shadow-primary/30 transition-all group-hover:-translate-y-1">
              <Plus className="w-8 h-8 stroke-[3]" />
            </div>
            <span className="text-xs font-bold text-slate-600">New Entity</span>
          </button>
          <button onClick={() => onNavigate('upload')} className="flex flex-col items-center gap-3 group">
            <div className="w-20 h-20 rounded-full bg-primary/20 border-2 border-primary/30 flex items-center justify-center text-primary transition-all group-hover:-translate-y-1">
              <UploadIcon className="w-8 h-8 stroke-[3]" />
            </div>
            <span className="text-xs font-bold text-slate-600">Upload</span>
          </button>
          <button className="flex flex-col items-center gap-3 group">
            <div className="w-20 h-20 rounded-full bg-primary/20 border-2 border-primary/30 flex items-center justify-center text-primary transition-all group-hover:-translate-y-1">
              <BarChart3 className="w-8 h-8 stroke-[3]" />
            </div>
            <span className="text-xs font-bold text-slate-600">Reports</span>
          </button>
        </div>
      </section>

      <section>
        <div className="flex items-center justify-between mb-5">
          <h4 className="text-slate-900 font-bold flex items-center gap-2">
            <History className="w-5 h-5 text-primary" /> Recent Activity
          </h4>
          <button className="text-primary text-sm font-bold">See All</button>
        </div>
        <div className="space-y-3">
          {activities.map((item) => (
            <div key={item.id} className="glass-card p-4 rounded-full flex items-center justify-between shadow-sm">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center">
                  {item.icon === 'business' && <Landmark className="w-5 h-5 text-slate-500" />}
                  {item.icon === 'store' && <Landmark className="w-5 h-5 text-slate-500" />}
                  {item.icon === 'rocket' && <Zap className="w-5 h-5 text-slate-500" />}
                </div>
                <div>
                  <p className="font-bold text-sm">{item.name}</p>
                  <p className="text-xs text-slate-400">{item.time}</p>
                </div>
              </div>
              <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${
                item.status === 'approved' ? 'bg-green-500/10 text-green-600' :
                item.status === 'processing' ? 'bg-amber-500/10 text-amber-600' :
                'bg-red-500/10 text-red-600'
              }`}>
                <span className={`w-1.5 h-1.5 rounded-full ${
                  item.status === 'approved' ? 'bg-green-500' :
                  item.status === 'processing' ? 'bg-amber-500' :
                  'bg-red-500'
                }`}></span>
                <span className="text-[10px] font-bold uppercase tracking-wider">{item.status}</span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </motion.div>
  );
};
