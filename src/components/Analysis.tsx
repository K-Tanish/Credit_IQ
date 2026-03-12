import React, { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { ShieldCheck, Loader2, AlertCircle, Cpu, TrendingUp, Lightbulb, Zap, Download, CheckCircle2 } from 'lucide-react';

export const Analysis = ({ currentEntity }: { currentEntity: any }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const caseId = currentEntity?.case_id;

  useEffect(() => {
    if (!caseId) {
      setLoading(false);
      return;
    }

    const fetchAnalysis = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/analysis/${caseId}`);
        if (!res.ok) throw new Error('Analysis not ready or case not found');
        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [caseId]);

  const handleDownload = () => {
    if (!caseId) return;
    window.open(`http://localhost:8000/api/v1/analysis/${caseId}/report`, '_blank');
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <Loader2 className="w-12 h-12 text-primary animate-spin" />
      <p className="text-slate-500 font-bold animate-pulse">Running Triangulation Engine...</p>
    </div>
  );

  if (!caseId || error || !data) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-6 text-center">
      <div className="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-6">
        <AlertCircle className="w-10 h-10 text-slate-400" />
      </div>
      <h2 className="text-2xl font-black text-slate-800 mb-2">Analysis Currently Unavailable</h2>
      <p className="text-slate-500 max-w-sm mb-4">
        {error ? `Reason: ${error}` : "We couldn't generate a report. Make sure you have uploaded and Approved at least 2 documents in the Upload section."}
      </p>
      {error && (
        <button 
          onClick={() => window.location.reload()}
          className="px-6 py-2 bg-slate-100 font-bold rounded-full text-slate-600 hover:bg-slate-200 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );

  const { credit_score, swot, findings, score_breakdown } = data;
  const isApproved = credit_score >= 70;

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 1.05 }}
      className="max-w-5xl mx-auto px-6 py-10 pb-32"
    >
      <section className="mb-10">
        <div className={`relative overflow-hidden flex flex-col items-center justify-center rounded-xl p-8 md:p-12 shadow-2xl transition-colors duration-700 ${isApproved ? 'bg-primary text-background-dark shadow-primary/20' : 'bg-red-500 text-white shadow-red-500/20'} group`}>
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <ShieldCheck className="w-32 h-32" />
          </div>
          <div className="z-10 text-center flex flex-col items-center gap-4">
            <p className="text-xs font-bold uppercase tracking-[0.2em] opacity-70">Real-Time Risk Assessment</p>
            <h1 className="text-4xl md:text-6xl font-extrabold tracking-tighter mb-2">
              {isApproved ? 'RECOMMENDATION: APPROVE' : 'RECOMMENDATION: REJECT'}
            </h1>
            <div className="bg-white/10 rounded-2xl px-10 py-6 backdrop-blur-md border border-white/10">
              <p className="text-lg font-medium opacity-80 mb-1 leading-none">CAMS Credit Score</p>
              <p className="text-[120px] font-black leading-none tracking-tighter">{credit_score}</p>
            </div>
            
            <div className="mt-8 grid grid-cols-3 gap-8 w-full max-w-lg">
              {Object.entries(score_breakdown).map(([key, val]: [string, any]) => (
                <div key={key} className="text-center">
                  <p className="text-[10px] uppercase font-bold opacity-60 mb-1">{key}</p>
                  <p className="text-2xl font-black">{val}%</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {findings.length > 0 && (
        <section className="mb-10">
          <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
            <Cpu className="w-4 h-4" /> Core Triangulation Findings
          </h3>
          <div className="space-y-3">
            {findings.map((f: any, i: number) => (
              <div key={i} className={`p-5 rounded-2xl border-l-4 flex gap-4 ${f.severity === 'HIGH' ? 'bg-red-50 border-red-500' : 'bg-emerald-50 border-emerald-500'}`}>
                {f.type === 'CONTRADICTION' ? <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0" /> : <CheckCircle2 className="w-6 h-6 text-emerald-500 flex-shrink-0" />}
                <div>
                  <h4 className="font-bold text-slate-900">{f.message}</h4>
                  <p className="text-sm text-slate-600 mt-1">{f.details}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SHAP Explainability (Pillar 5) */}
      {data.external_intelligence?.pd_model?.shap_summary && (
        <section className="mb-10">
          <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-primary" /> AI Explainability (SHAP Factors)
          </h3>
          <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-bold text-slate-600">Probability of Default (PD)</span>
              <span className="text-xl font-black text-slate-900">{data.external_intelligence.pd_model.pd_percentage}%</span>
            </div>
            <div className="space-y-3">
              {Object.entries(data.external_intelligence.pd_model.shap_summary).map(([key, val]: [string, any]) => (
                <div key={key} className="space-y-1">
                  <div className="flex justify-between text-[11px] font-bold uppercase tracking-tight text-slate-500">
                    <span>{key}</span>
                    <span className={val >= 0 ? 'text-emerald-500' : 'text-red-500'}>
                      {val >= 0 ? '+' : ''}{val} pts
                    </span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.abs(val) * 2}%` }}
                      className={`h-full rounded-full ${val >= 0 ? 'bg-emerald-400' : 'bg-red-400'}`}
                    />
                  </div>
                </div>
              ))}
            </div>
            <p className="text-[10px] italic text-slate-400 mt-4 leading-relaxed">
              * This model uses an XGBoost architecture with SHAP (SHapley Additive exPlanations) values to distribute the weight of each risk factor toward the base credit score.
            </p>
          </div>
        </section>
      )}

      {/* External Intelligence (Pillar 5) */}
      {data.external_intelligence?.news?.length > 0 && (
        <section className="mb-10">
          <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-primary" /> Secondary Intelligence (Pillar 5)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.external_intelligence.news.map((n: any, i: number) => (
              <div key={i} className="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-black uppercase tracking-wider text-slate-400">{n.source}</span>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${n.sentiment === 'Negative' ? 'bg-red-50 text-red-500' : 'bg-emerald-50 text-emerald-500'}`}>
                    {n.sentiment}
                  </span>
                </div>
                <p className="font-bold text-slate-800 text-sm">{n.title}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="mb-10">
        <div className="bg-[#E1DEC9] p-8 md:p-10 rounded-xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-extrabold tracking-tight text-slate-800">SWOT Analysis</h2>
            <div className="flex gap-2 items-center">
              <div className="w-3 h-3 rounded-full bg-slate-900 animate-pulse"></div>
              <span className="text-xs font-bold uppercase tracking-widest text-slate-600">Generated from Evidence</span>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[
              { title: 'Strengths', icon: TrendingUp, color: 'emerald', items: swot.strengths },
              { title: 'Weaknesses', icon: AlertCircle, color: 'red', items: swot.weaknesses },
              { title: 'Opportunities', icon: Lightbulb, color: 'blue', items: swot.opportunities },
              { title: 'Threats', icon: Zap, color: 'amber', items: swot.threats },
            ].map((s) => (
              <div key={s.title} className="bg-white/40 backdrop-blur-md border border-white/60 p-6 rounded-3xl shadow-sm relative overflow-hidden group hover:shadow-xl transition-all duration-500 min-h-[160px]">
                <div className="flex items-center gap-3 mb-4">
                  <div className={`w-10 h-10 rounded-2xl bg-${s.color}-100 flex items-center justify-center text-${s.color}-600 shadow-md`}>
                    <s.icon className="w-6 h-6" />
                  </div>
                  <h3 className="font-extrabold text-lg text-slate-800">{s.title}</h3>
                </div>
                <ul className="space-y-3">
                  {s.items.length > 0 ? s.items.map((item: string) => (
                    <li key={item} className="flex items-start gap-2 text-sm font-semibold text-slate-700">
                      <div className={`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 bg-${s.color}-500`}></div>
                      <span>{item}</span>
                    </li>
                  )) : (
                    <p className="text-xs italic text-slate-400">No data points detected</p>
                  )}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="flex justify-center gap-4">
        <button 
          onClick={handleDownload}
          className="flex items-center gap-2 px-8 py-4 bg-slate-900 text-white rounded-full font-bold shadow-xl hover:-translate-y-1 transition-all"
        >
          <Download className="w-5 h-5" /> Download Full Memo
        </button>
      </div>
    </motion.div>
  );
};
