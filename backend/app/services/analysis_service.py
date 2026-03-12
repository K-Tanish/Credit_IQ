import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.document import Document
from ..models.analysis import Analysis
import uuid
from ..services.research_service import research_service
from ..services.scoring_engine import ai_scoring_engine
from ..models.entity import Entity
from ..services.ai_agent import swot_agent

class TriangulationEngine:
    """
    Pillar 3 Service: Compares data across approved documents
    to find contradictions and calculate real credit risk.
    """

    def extract_figures(self, text: str) -> Dict[str, float]:
        """Simple regex extraction of financial figures from OCR/Text"""
        results = {}
        # Look for Turnover/Sales
        turnover_match = re.search(r"(?:Total|Annual)\s+(?:Turnover|Sales|Revenue).*?(\d[\d,.]*)", text, re.I)
        if turnover_match:
            val = turnover_match.group(1).replace(",", "")
            try: results['turnover'] = float(val)
            except: pass
            
        # Look for GST amounts
        gst_match = re.search(r"(?:GST|CGST|SGST)\s+(?:Payable|Total).*?(\d[\d,.]*)", text, re.I)
        if gst_match:
            val = gst_match.group(1).replace(",", "")
            try: results['gst_total'] = float(val)
            except: pass
            
        return results

    async def run_analysis(self, db: Session, case_id: str) -> Analysis:
        # 1. Get all approved documents for this case
        entity = db.query(Entity).filter(Entity.case_id == case_id).first()
        if not entity: raise ValueError("Entity not found")

        docs = db.query(Document).filter(
            Document.case_id == case_id,
            Document.status == "approved"
        ).all()

        # 2. Consolidate structured data from all docs
        extracted_data = {}
        for doc in docs:
            label = doc.user_label or doc.auto_label
            # Merge extracted_data into our analysis map
            if doc.extracted_data:
                extracted_data[label] = doc.extracted_data

        # 3. Perform Contradiction Checks (Triangulation)
        findings = []
        base_score = 70 # Default neutral score
        
        # Check 1: GST Sales vs Bank Credits (Proxy for undeclared income)
        gst_data = extracted_data.get("GST Return", {})
        bank_data = extracted_data.get("Bank Statement", {})
        
        # We compare GST turnover with Bank Total Credits
        gst_val = gst_data.get('turnover')
        bank_val = bank_data.get('total_credits')
        
        if gst_val and bank_val:
            diff = abs(gst_val - bank_val)
            max_val = max(gst_val, bank_val, 1)
            variance = diff / max_val
            
            # Feature for PD model
            turnover_variance_feat = variance
            
            if variance > 0.15: # > 15% variance is a red flag
                findings.append({
                    "type": "CONTRADICTION",
                    "severity": "HIGH",
                "message": f"Turnover mismatch of {variance:.1%} detected between GST and Bank records.",
                "details": f"GST: {gst_data.get('turnover')}, Bank: {bank_data.get('total_credits')}"
                })
                base_score -= 20
            else:
                findings.append({
                    "type": "CONFIRMATION",
                    "severity": "LOW",
                    "message": "GST and Bank Statement turnover is consistent.",
                    "details": f"Variance: {variance:.1%}"
                })
                base_score += 10
        else:
            turnover_variance_feat = 0.0

        # Check 2: Pillar 3 - OD Window Dressing (Bank Balance logic)
        # If closing balance is significantly higher than total credits, it might be window dressing
        if bank_data.get('closing_balance') and bank_data.get('total_credits'):
            balance_ratio = bank_data['closing_balance'] / max(bank_data['total_credits'], 1)
            if balance_ratio > 0.8: # Suggests almost all credits are sitting as balance at month end
                findings.append({
                    "type": "WARNING",
                    "severity": "MEDIUM",
                    "message": "Potential OD Window Dressing detected.",
                    "details": "Closing balance exceeds 80% of total credits for the period."
                })
                base_score -= 5
 
        # Check 3: Promoter Pledge Concentration (Shareholding Pattern)
        shareholding_data = extracted_data.get("Shareholding Pattern", {})
        pledge_pct = shareholding_data.get("promoter_pledge_pct", 0)
        if pledge_pct > 25:
            findings.append({
                "type": "CONCENTRATION_RISK",
                "severity": "HIGH" if pledge_pct > 50 else "MEDIUM",
                "message": f"High Promoter Pledge detected: {pledge_pct}%",
                "details": "High levels of pledged shares increase the risk of margin calls and management instability."
            })
            base_score -= 10 if pledge_pct > 50 else 5

        # Check 4: ALM Bucket Mismatch (Asset Liability Management)
        alm_data = extracted_data.get("ALM Report", {})
        gap_30d = alm_data.get("gap_1_to_30_days", 0)
        gap_90d = alm_data.get("gap_31_to_90_days", 0)
        
        if gap_30d < 0 or gap_90d < 0:
            findings.append({
                "type": "LIQUIDITY_STRESS",
                "severity": "HIGH",
                "message": "Short-term ALM Mismatch detected (Negative Gap).",
                "details": f"1-30 days gap: {gap_30d}, 31-90 days gap: {gap_90d}. Indicates potential cash flow crunch."
            })
            base_score -= 15

        # Check 3: Pillar 5 External Intelligence (News/Litigation)

        # Check 3: Pillar 5 External Intelligence (News/Litigation)
        try:
            news = await research_service.get_negative_news(entity.company_name)
            litigation = await research_service.get_litigation_status(entity.cin)
        except Exception as e:
            print(f"External Intelligence failed: {e}")
            news = []
            litigation = {"status": "Unknown (Service Error)"}
        
        for n in news:
            if n['sentiment'] == "Negative":
                findings.append({
                    "type": "SECONDARY_SIGNAL",
                    "severity": "MEDIUM",
                    "message": f"Negative news alert: {n['title']}",
                    "details": f"Source: {n['source']}"
                })
                base_score -= 5
            elif n['sentiment'] == "Positive":
                base_score += 2

        # 4. Integrate Pillar 5 XGBoost PD Model
        features = {
            "turnover_variance": turnover_variance_feat,
            "has_negative_news": any(n['sentiment'] == "Negative" for n in news),
            "sector": entity.sector,
            "docs_approved_pct": len(docs) / 4.0 # Benchmark against 4 ideal docs
        }
        pd_analysis = ai_scoring_engine.calculate_pd(features)
        base_score = pd_analysis['cams_score']

        # 5. Generate AI-Powered SWOT
        entity_profile = {
            "company_name": entity.company_name,
            "sector": entity.sector,
            "loan_amount": entity.loan_amount,
            "loan_type": entity.loan_type
        }
        doc_texts = [d.extracted_text for d in docs if d.extracted_text]
        swot = await swot_agent.generate_swot(entity_profile, findings, doc_texts)

        # 5. Persist Analysis
        analysis = db.query(Analysis).filter(Analysis.case_id == case_id).first()
        if not analysis:
            analysis = Analysis(id=str(uuid.uuid4()), case_id=case_id)
            db.add(analysis)

        analysis.credit_score = min(max(base_score, 0), 100)
        analysis.findings = findings
        analysis.swot = swot
        analysis.external_intelligence = {
            "news": news, 
            "litigation": litigation,
            "pd_model": pd_analysis
        }
        analysis.score_breakdown = {
            "financial": min(base_score + 5, 100),
            "compliance": 90 if not [f for f in findings if "GST" in f['message']] else 60,
            "verification": 100 if len(docs) >= 3 else 70
        }
        
        db.commit()
        db.refresh(analysis)
        return analysis

analysis_engine = TriangulationEngine()
