export type Screen = 'dashboard' | 'onboarding' | 'loading' | 'analysis' | 'upload';

export interface ActivityItem {
  id: string;
  name: string;
  time: string;
  status: 'approved' | 'processing' | 'rejected';
  icon: 'business' | 'store' | 'rocket';
}

export interface DocumentRequirement {
  id: string;
  name: string;
  status: 'pending' | 'detected';
  description: string;
  fileName?: string;
  icon: 'description' | 'pie_chart' | 'query_stats';
}

/** Matches DocumentResponse from the backend */
export interface UploadedDocument {
  id: string;
  entity_id: string;
  filename: string;
  file_type: string | null;
  file_size: number | null;
  auto_label: string | null;
  user_label: string | null;
  confidence_score: number | null;
  status: string;
  extracted_text?: string | null;
  extracted_data?: Record<string, any>;
  created_at: string;
  updated_at?: string | null;
}
