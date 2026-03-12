import React from 'react';
import { BarChart3, Bell } from 'lucide-react';
import { Screen } from '../../types';

export const Navbar = ({ onNavigate }: { onNavigate: (s: Screen) => void }) => (
  <header className="flex items-center justify-between px-6 py-5 max-w-4xl mx-auto w-full relative z-10">
    <div className="flex items-center gap-3 cursor-pointer" onClick={() => onNavigate('dashboard')}>
      <div className="bg-primary p-2 rounded-lg flex items-center justify-center">
        <BarChart3 className="w-6 h-6 text-background-dark" />
      </div>
      <h1 className="text-xl font-extrabold tracking-tight">Credit_IQ</h1>
    </div>
    <div className="flex items-center gap-3">
      <button className="w-11 h-11 flex items-center justify-center rounded-full bg-slate-200/50 text-slate-700">
        <Bell className="w-5 h-5" />
      </button>
      <div className="w-11 h-11 rounded-full bg-primary/20 border-2 border-primary overflow-hidden">
        <img 
          alt="User Profile" 
          className="w-full h-full object-cover" 
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuApTZpZoWPCLbp3Own-Rs6g-4zVL92j_B7zp6mGxKNA6d96VfiW-MVlSUPvAKBuhbhQBf-LEvzW-d-6XCx_PClQc9_owoARyqgQPEuXlhH8qftO--i6Trr1DHWfRsFYji-Q2GajyIJkqZgEKscWWEWThe35yuvh-98zlGT2tXq4DTLkVTy68Rn6mKlYcUJmB41J3I0RFbx-rbOj1cNEh78ifRaPMnPTO6NLTkEYRUmbis-ZKKV5j0aGL7Juzey1BkvhDdu3kMXxYWs" 
          referrerPolicy="no-referrer"
        />
      </div>
    </div>
  </header>
);
