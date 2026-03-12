import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { AlertCircle, X, TrendingUp, Landmark, ChevronRight, Loader2 } from 'lucide-react';

export const Onboarding = ({ onNext }: { onNext: (data: any) => void }) => {
  const [formData, setFormData] = useState({
    company_name: '',
    cin: '',
    pan: '',
    sector: 'manufacturing',
    annual_turnover: 0,
    net_worth: 0,
    loan_amount: 0,
    loan_type: 'term_loan',
    tenure_months: 12
  });
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleSubmit = async () => {
    setErrorMsg(null);

    // Client-side required field check
    if (!formData.company_name.trim()) {
      setErrorMsg('Company Name is required.');
      return;
    }
    if (!formData.cin.trim()) {
      setErrorMsg('CIN Number is required.');
      return;
    }
    if (!formData.pan.trim()) {
      setErrorMsg('Business PAN is required.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/entities/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          cin: formData.cin.trim().toUpperCase(),
          pan: formData.pan.trim().toUpperCase(),
        }),
      });
      if (response.ok) {
        const data = await response.json();
        onNext(data);
      } else {
        const err = await response.json();
        if (Array.isArray(err.detail)) {
          const msgs = err.detail.map((e: any) => {
            const field = e.loc?.slice(1).join('.') ?? 'field';
            return `${field}: ${e.msg}`;
          }).join(' · ');
          setErrorMsg(msgs);
        } else {
          setErrorMsg(err.detail || 'Failed to onboard entity. Please check your inputs.');
        }
      }
    } catch (error) {
      setErrorMsg('Could not connect to backend. Make sure Docker is running (docker-compose up).');
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="max-w-3xl mx-auto px-6 py-10"
    >
      <div className="flex flex-col gap-4 mb-10">
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 bg-primary/20 text-slate-800 rounded-full text-xs font-bold uppercase tracking-wider">Onboarding</span>
          <span className="text-slate-400 text-sm font-medium">Step 1 of 3</span>
        </div>
        <h1 className="text-slate-900 tracking-tight text-4xl md:text-5xl font-extrabold leading-[1.1]">
          Let's tap into the <span className="text-primary">details.</span>
        </h1>
        <p className="text-slate-500 text-lg">We need a few details to verify your business and customize your credit experience.</p>
      </div>

      {/* Inline error banner */}
      <AnimatePresence>
        {errorMsg && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="flex items-start gap-3 mb-8 p-4 rounded-2xl bg-red-50 border border-red-200 text-red-700"
          >
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-bold text-sm">Submission Error</p>
              <p className="text-sm mt-0.5">{errorMsg}</p>
            </div>
            <button onClick={() => setErrorMsg(null)} className="ml-auto flex-shrink-0 text-red-400 hover:text-red-600">
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      <section className="flex flex-col gap-8 mb-12">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 bg-primary rounded-full"></div>
          <h3 className="text-slate-900 text-xl font-bold">Entity Authentication</h3>
        </div>
        <div className="space-y-6">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-bold text-slate-500 ml-4">Company Name <span className="text-red-400">*</span></label>
            <input 
              value={formData.company_name}
              onChange={(e) => setFormData({...formData, company_name: e.target.value})}
              className="pill-input w-full bg-white border-none rounded-full px-6 py-4 text-slate-900 placeholder:text-slate-300 focus:ring-2 focus:ring-primary transition-all text-lg" placeholder="e.g. Acme Tech Solutions Pvt Ltd" type="text"/>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1">
              <label className="text-sm font-bold text-slate-500 ml-4">CIN Number <span className="text-red-400">*</span></label>
              <input 
                value={formData.cin}
                onChange={(e) => setFormData({...formData, cin: e.target.value})}
                className="pill-input w-full bg-white border-none rounded-full px-6 py-4 text-slate-900 placeholder:text-slate-300 focus:ring-2 focus:ring-primary transition-all uppercase" placeholder="U74999MH2023PTC456789" type="text"/>
              <p className="text-xs text-slate-400 ml-4">Format: U/L + 5 digits + 2 letters + 4 digits + 3 letters + 6 digits</p>
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-sm font-bold text-slate-500 ml-4">Business PAN <span className="text-red-400">*</span></label>
              <input 
                value={formData.pan}
                onChange={(e) => setFormData({...formData, pan: e.target.value})}
                className="pill-input w-full bg-white border-none rounded-full px-6 py-4 text-slate-900 placeholder:text-slate-300 focus:ring-2 focus:ring-primary transition-all uppercase" placeholder="ABCDE1234F" type="text"/>
              <p className="text-xs text-slate-400 ml-4">Format: 5 letters + 4 digits + 1 letter (e.g. ABCDE1234F)</p>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-sm font-bold text-slate-500 ml-4">Entity Sector</label>
            <select 
              value={formData.sector}
              onChange={(e) => setFormData({...formData, sector: e.target.value})}
              className="pill-input w-full bg-white border-none rounded-full px-6 py-4 text-slate-900 appearance-none focus:ring-2 focus:ring-primary transition-all text-lg cursor-pointer">
              <option value="manufacturing">Manufacturing</option>
              <option value="infrastructure">Infrastructure &amp; Construction</option>
              <option value="it_services">IT &amp; Digital Services</option>
              <option value="retail">Retail &amp; E-commerce</option>
              <option value="healthcare">Healthcare &amp; Pharma</option>
              <option value="textiles">Textiles &amp; Apparel</option>
            </select>
          </div>
        </div>
      </section>

      <section className="flex flex-col gap-8 mb-12">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 bg-primary rounded-full"></div>
          <h3 className="text-slate-900 text-xl font-bold">Loan Parameters</h3>
        </div>
        <div className="space-y-6">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-bold text-slate-500 ml-4">Requested Loan Amount</label>
            <div className="relative">
              <span className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-lg">₹</span>
              <input 
                value={formData.loan_amount || ''}
                onChange={(e) => setFormData({...formData, loan_amount: Number(e.target.value)})}
                className="pill-input w-full bg-white border-none rounded-full pl-12 pr-6 py-4 text-slate-900 placeholder:text-slate-300 focus:ring-2 focus:ring-primary transition-all text-lg font-bold" placeholder="e.g. 5000000" type="number"/>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-bold text-slate-500 ml-4">Loan Type</label>
              <select 
                value={formData.loan_type}
                onChange={(e) => setFormData({...formData, loan_type: e.target.value})}
                className="pill-input w-full bg-white border-none rounded-full px-6 py-4 text-slate-900 appearance-none focus:ring-2 focus:ring-primary transition-all text-base cursor-pointer">
                <option value="wc_limit">Working Capital Limit</option>
                <option value="term_loan">Term Loan</option>
                <option value="lc_bg">LC / BG (Non-Fund Based)</option>
                <option value="od_limit">Overdraft Limit</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-bold text-slate-500 ml-4">Tenure (Months)</label>
              <input 
                value={formData.tenure_months}
                onChange={(e) => setFormData({...formData, tenure_months: Number(e.target.value)})}
                className="pill-input w-full bg-white border-none rounded-full px-6 py-4 text-slate-900 placeholder:text-slate-300 focus:ring-2 focus:ring-primary transition-all" placeholder="e.g. 12" type="number"/>
            </div>
          </div>
        </div>
      </section>

      <section className="flex flex-col gap-8 mb-12">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 bg-primary rounded-full"></div>
          <h3 className="text-slate-900 text-xl font-bold">Financial Profile</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="pill-input bg-white p-6 rounded-3xl flex flex-col gap-4 border border-transparent hover:border-primary/30 transition-all group">
            <div className="w-12 h-12 bg-primary/10 rounded-2xl flex items-center justify-center text-primary">
              <TrendingUp className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-500">Annual Turnover</p>
              <p className="text-xs text-slate-400 mt-1">Estimates for the last FY</p>
            </div>
            <div className="relative">
              <span className="absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 font-bold">₹</span>
              <input 
                value={formData.annual_turnover || ''}
                onChange={(e) => setFormData({...formData, annual_turnover: Number(e.target.value)})}
                className="w-full bg-transparent border-b-2 border-slate-100 focus:border-primary focus:ring-0 pl-4 py-2 text-xl font-bold text-slate-900" placeholder="e.g. 25000000" type="number"/>
            </div>
          </div>
          <div className="pill-input bg-white p-6 rounded-3xl flex flex-col gap-4 border border-transparent hover:border-primary/30 transition-all group">
            <div className="w-12 h-12 bg-primary/10 rounded-2xl flex items-center justify-center text-primary">
              <Landmark className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-500">Estimated Net Worth</p>
              <p className="text-xs text-slate-400 mt-1">Total assets minus liabilities</p>
            </div>
            <div className="relative">
              <span className="absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 font-bold">₹</span>
              <input 
                value={formData.net_worth || ''}
                onChange={(e) => setFormData({...formData, net_worth: Number(e.target.value)})}
                className="w-full bg-transparent border-b-2 border-slate-100 focus:border-primary focus:ring-0 pl-4 py-2 text-xl font-bold text-slate-900" placeholder="e.g. 10000000" type="number"/>
            </div>
          </div>
        </div>
      </section>

      <div className="flex flex-col items-center gap-6 pb-20">
        <button 
          onClick={handleSubmit}
          disabled={loading}
          className={`w-20 h-20 bg-primary hover:scale-105 active:scale-95 transition-all rounded-full flex items-center justify-center shadow-lg shadow-primary/40 group ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {loading ? (
            <Loader2 className="w-10 h-10 text-slate-900 animate-spin" />
          ) : (
            <ChevronRight className="w-10 h-10 text-slate-900 group-hover:translate-x-1 transition-transform" />
          )}
        </button>
        <p className="text-slate-400 text-sm font-medium">Press <kbd className="px-2 py-1 bg-slate-100 rounded-md border border-slate-200 text-xs">Enter</kbd> to continue</p>
      </div>
    </motion.div>
  );
};
