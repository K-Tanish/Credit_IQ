import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  ScanLine, CloudUpload, Loader2, AlertCircle, X, Info, 
  FileText, Tag, Pencil, CheckCheck, ThumbsDown, ThumbsUp, 
  ChevronDown, Cpu, Zap, Database 
} from 'lucide-react';
import { UploadedDocument } from '../types';

const DOCUMENT_LABELS = [
  'ALM Report', 'Balance Sheet', 'Bank Statement', 'GST Return',
  'ITR Filing', 'Profit & Loss Statement', 'Shareholding Pattern',
  'Credit Report', 'Audit Report', 'KYC Document', 'Borrowing Profile', 'MCA Filing',
];

const ACCEPTED_TYPES = '.pdf,.xls,.xlsx,.csv,.png,.jpg,.jpeg,.tiff,.bmp';

function ConfidencePill({ score }: { score: number | null }) {
  if (score === null) return null;
  const pct = Math.round(score * 100);
  const color = pct >= 80 ? 'text-emerald-600 bg-emerald-50 border-emerald-200'
    : pct >= 55 ? 'text-amber-600 bg-amber-50 border-amber-200'
    : 'text-red-500 bg-red-50 border-red-200';
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-bold border ${color}`}>
      <Cpu className="w-3 h-3" />
      {pct}% confidence
    </span>
  );
}

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, string> = {
    classified: 'bg-blue-100 text-blue-700',
    pending_review: 'bg-amber-100 text-amber-700',
    approved: 'bg-emerald-100 text-emerald-700',
    rejected: 'bg-red-100 text-red-600',
    uploaded: 'bg-slate-100 text-slate-600',
  };
  return (
    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider ${map[status] ?? 'bg-slate-100 text-slate-500'}`}>
      {status.replace('_', ' ')}
    </span>
  );
}

function DocCard({ doc, onReview }: { doc: UploadedDocument, onReview: (d: UploadedDocument) => void }) {
  const label = doc.user_label ?? doc.auto_label ?? 'Unclassified';
  const isApproved = doc.status === 'approved';
  const isRejected = doc.status === 'rejected';

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className={`relative overflow-hidden bg-white rounded-2xl border shadow-sm transition-all group
        ${isApproved ? 'border-emerald-200' : isRejected ? 'border-red-200' : 'border-slate-100 hover:border-primary/40'}`}
    >
      <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-2xl
        ${isApproved ? 'bg-emerald-400' : isRejected ? 'bg-red-400' : 'bg-primary/60'}`} />

      <div className="pl-5 pr-4 py-4 flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 min-w-0">
          <div className={`mt-0.5 w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center
            ${isApproved ? 'bg-emerald-100 text-emerald-600' : isRejected ? 'bg-red-100 text-red-500' : 'bg-primary/10 text-primary'}`}>
            <FileText className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <p className="font-bold text-slate-900 text-sm truncate" title={doc.filename}>{doc.filename}</p>
            <div className="flex flex-wrap items-center gap-2 mt-1">
              <span className="flex items-center gap-1 text-xs font-semibold text-slate-500">
                <Tag className="w-3 h-3" /> {label}
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2 mt-2">
              <StatusBadge status={doc.status} />
              <ConfidencePill score={doc.confidence_score} />
              {doc.extracted_data && Object.keys(doc.extracted_data).length > 0 && (
                <span className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-600 border border-indigo-100">
                  <Database className="w-3 h-3" />
                  {Object.keys(doc.extracted_data).length} values extracted
                </span>
              )}
            </div>
            {doc.extracted_data && Object.keys(doc.extracted_data).length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {Object.entries(doc.extracted_data).slice(0, 3).map(([key, val]) => (
                  <div key={key} className="bg-slate-50 border border-slate-100 rounded-lg px-2 py-1 flex items-center gap-1.5">
                    <span className="text-[10px] font-bold uppercase text-slate-400">{key.replace('_', ' ')}</span>
                    <span className="text-xs font-black text-slate-700">₹{typeof val === 'number' ? val.toLocaleString() : val}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        {!isApproved && !isRejected && (
          <button
            onClick={() => onReview(doc)}
            className="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-100 hover:bg-primary hover:text-background-dark text-slate-500 text-xs font-bold transition-all"
          >
            <Pencil className="w-3.5 h-3.5" /> Review
          </button>
        )}
      </div>
    </motion.div>
  );
}

function ReviewModal({ doc, onClose, onSave }: any) {
  const [selectedLabel, setSelectedLabel] = useState(doc.user_label ?? doc.auto_label ?? '');
  const [isOpen, setIsOpen] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleAction = async (status: 'approved' | 'rejected') => {
    setSaving(true);
    await onSave(doc.id, { user_label: selectedLabel, status });
    setSaving(false);
    onClose();
  };

  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-slate-900/40 backdrop-blur-sm px-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="bg-white w-full max-w-md rounded-3xl shadow-2xl p-6 space-y-5"
        initial={{ y: 60, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 40, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between">
          <h3 className="font-extrabold text-lg text-slate-900">HITL Classification Review</h3>
          <button onClick={onClose} className="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 text-slate-500 hover:bg-slate-200">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="bg-slate-50 rounded-2xl p-4 space-y-2">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">File</p>
          <p className="font-bold text-slate-800 text-sm truncate">{doc.filename}</p>
        </div>

        <div>
          <p className="text-sm font-bold text-slate-700 mb-2">Override Document Type</p>
          <div className="relative">
            <button
              type="button"
              onClick={() => setIsOpen(!isOpen)}
              className="w-full flex items-center justify-between px-4 py-3 bg-white border-2 border-slate-200 rounded-xl text-sm font-semibold text-slate-800 hover:border-primary transition-colors"
            >
              {selectedLabel || 'Select a document type…'}
              <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>
            {isOpen && (
              <div className="absolute z-10 mt-1 w-full bg-white border border-slate-200 rounded-xl shadow-xl max-h-56 overflow-y-auto">
                {DOCUMENT_LABELS.map((l) => (
                  <button
                    key={l}
                    type="button"
                    onClick={() => { setSelectedLabel(l); setIsOpen(false); }}
                    className={`w-full text-left px-4 py-2.5 text-sm font-medium hover:bg-primary/5 transition-colors
                      ${selectedLabel === l ? 'text-primary font-bold' : 'text-slate-700'}`}
                  >
                    {l}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="flex gap-3 pt-1">
          <button
            onClick={() => handleAction('rejected')}
            disabled={saving}
            className="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl border-2 border-red-200 text-red-500 font-bold hover:bg-red-50 transition-colors disabled:opacity-50"
          >
            <ThumbsDown className="w-4 h-4" /> Reject
          </button>
          <button
            onClick={() => handleAction('approved')}
            disabled={saving || !selectedLabel}
            className="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl bg-primary text-background-dark font-bold hover:scale-[1.02] transition-all disabled:opacity-50 shadow-lg shadow-primary/20"
          >
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <ThumbsUp className="w-4 h-4" />}
            Approve
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

export const Upload = ({ onProcess, currentEntity }: { onProcess: () => void; currentEntity: any }) => {
  const [docs, setDocs] = useState<UploadedDocument[]>([]);
  const [uploading, setUploading] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [reviewTarget, setReviewTarget] = useState<UploadedDocument | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fetchedCaseId, setFetchedCaseId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const caseId: string | null = currentEntity?.case_id ?? null;

  useEffect(() => {
    if (!caseId || caseId === fetchedCaseId) return;
    setFetchedCaseId(caseId);
    fetch(`http://localhost:8000/api/v1/documents/${caseId}`)
      .then(r => r.ok ? r.json() : [])
      .then(setDocs)
      .catch(() => {});
  }, [caseId, fetchedCaseId]);

  const uploadFile = useCallback(async (file: File) => {
    if (!caseId) {
      setError('No active entity. Please onboard an entity first.');
      return;
    }
    setUploading(true);
    setError(null);
    try {
      const fd = new FormData();
      fd.append('file', file);
      const res = await fetch(`http://localhost:8000/api/v1/documents/upload/${caseId}`, {
        method: 'POST',
        body: fd,
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        setError(body.detail ?? 'Upload failed');
        return;
      }
      const newDoc: UploadedDocument = await res.json();
      setDocs(prev => [newDoc, ...prev]);
    } catch {
      setError('Could not connect to backend. Make sure Docker is running.');
    } finally {
      setUploading(false);
    }
  }, [caseId]);

  const handleFiles = useCallback((files: FileList | null) => {
    if (!files) return;
    Array.from(files).forEach(uploadFile);
  }, [uploadFile]);

  const handleReviewSave = async (id: string, payload: any) => {
    const res = await fetch(`http://localhost:8000/api/v1/documents/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      const updated: UploadedDocument = await res.json();
      setDocs(prev => prev.map(d => d.id === id ? updated : d));
    }
  };

  const pendingCount = docs.filter(d => d.status === 'pending_review' || d.status === 'classified').length;
  const approvedCount = docs.filter(d => d.status === 'approved').length;

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="max-w-2xl mx-auto px-4 py-8 pb-36"
      >
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <ScanLine className="w-5 h-5 text-primary" />
            <span className="text-xs font-extrabold uppercase tracking-widest text-slate-400">Pillar 2</span>
          </div>
          <h1 className="text-5xl font-black tracking-tighter text-slate-900 leading-[0.9] mb-2">
            Intelligent <span className="text-primary">Document</span> Ingestion
          </h1>
          <p className="text-slate-500 font-medium">
            {caseId ? (
              <>Case: <span className="font-bold text-slate-700">{caseId}</span></>
            ) : (
              <span className="text-amber-600 font-semibold">⚠ Onboard an entity first to enable uploads</span>
            )}
          </p>
        </div>

        <div
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => { e.preventDefault(); setDragging(false); handleFiles(e.dataTransfer.files); }}
          onClick={() => !uploading && caseId && fileInputRef.current?.click()}
          className={`relative mb-6 flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed py-10 px-6 transition-all cursor-pointer
            ${dragging ? 'border-primary bg-primary/5 scale-[1.01]' : 'border-slate-200 bg-white hover:border-primary/60 hover:bg-primary/5'}
            ${!caseId ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input ref={fileInputRef} type="file" accept={ACCEPTED_TYPES} multiple className="hidden" onChange={(e) => handleFiles(e.target.files)} />
          <CloudUpload className="w-7 h-7 text-slate-400" />
          <p className="font-bold text-slate-700 text-sm">Drop files here or click to browse</p>
        </div>

        {docs.length > 0 && (
          <div className="space-y-3">
            {docs.map(doc => <DocCard key={doc.id} doc={doc} onReview={setReviewTarget} />)}
          </div>
        )}
      </motion.div>

      {approvedCount > 0 && (
        <div className="fixed bottom-24 left-0 w-full flex justify-center px-6 pointer-events-none z-40">
          <button
            onClick={onProcess}
            className="pointer-events-auto flex items-center gap-3 px-8 py-4 bg-primary text-background-dark rounded-full font-black text-lg shadow-2xl hover:scale-105 transition-transform active:scale-95 group"
          >
            <span>Process {approvedCount} Document{approvedCount > 1 ? 's' : ''}</span>
            <Zap className="w-6 h-6 group-hover:translate-x-1 transition-transform fill-background-dark" />
          </button>
        </div>
      )}

      <AnimatePresence>
        {reviewTarget && <ReviewModal doc={reviewTarget} onClose={() => setReviewTarget(null)} onSave={handleReviewSave} />}
      </AnimatePresence>
    </>
  );
};
