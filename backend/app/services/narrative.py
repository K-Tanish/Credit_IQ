from typing import Dict, Any, List

class NarrativeEngine:
    """
    Pillar 5 Narrative Engine: Converts structured financial and risk data
    into professional, human-readable text for the final Credit Memo.
    """

    def generate_background(self, entity: Dict[str, Any]) -> str:
        """Section 1: Company Background"""
        return (
            f"{entity.get('company_name')} is a business entity operating within the "
            f"{entity.get('sector', 'unspecified')} sector. Identified by CIN {entity.get('cin')} "
            f"and PAN {entity.get('pan')}, the organization has sought credit assessment "
            f"for a loan requirement of Rs.{entity.get('loan_amount', 'N/A')} "
            f"({entity.get('loan_type', 'Term Loan')}). The initial financial profiling "
            f"indicates a turnover of Rs.{entity.get('turnover', 'N/A')} with a net worth of "
            f"Rs.{entity.get('net_worth', 'N/A')}."
        )

    def generate_research_summary(self, findings: List[Dict[str, Any]], docs: List[Any]) -> str:
        """Section 2: Quality Research (Triangulation)"""
        doc_names = [d.filename for d in docs]
        summary = (
            f"A deep-dive triangulation analysis was performed using {len(docs)} verified sources, "
            f"including {', '.join(doc_names[:3])}. "
        )
        
        high_severity = [f for f in findings if f.get('severity') == 'HIGH']
        if high_severity:
            summary += (
                f"Critical discrepancies were identified during the cross-verification process. "
                f"Specifically, {high_severity[0].get('message')}. "
            )
        else:
            summary += "The cross-document verification indicates a high degree of financial reporting consistency across GST and banking channels. "
            
        # Add ALM/Pledge context
        if any('ALM' in f.get('message', '') for f in findings):
            summary += "Short-term liquidity analysis reveals pressure points in the 0-90 day buckets. "
        if any('Pledge' in f.get('message', '') for f in findings):
            summary += "Capital structure analysis notes significant promoter share encumbrance. "
            
        return summary

    def generate_external_intelligence(self, external: Dict[str, Any]) -> str:
        """Section 3: News, Legal, Market Sentiment"""
        news = external.get('news', [])
        litigation = external.get('litigation', {})
        
        intro = "Secondary intelligence gathering via external digital footprints provides a comprehensive 'Market View' of the entity. "
        
        neg_news = [n for n in news if n.get('sentiment') == 'Negative']
        if neg_news:
            news_text = f"Adverse news signals were detected, notably regarding '{neg_news[0].get('title')}', suggesting localized reputational or regulatory headwinds. "
        else:
            news_text = "Market sentiment across primary financial news outlets remains stable to positive, with no major adverse triggers detected. "
            
        lit_text = "Legal compliance checks indicate " + (litigation.get('status', 'no major active litigation').lower()) + ". "
        
        return intro + news_text + lit_text

    def generate_final_verdict(self, score: int, findings: List[Dict[str, Any]]) -> str:
        """Section 4: Final Concerns & Verdict"""
        high_risks = [f for f in findings if f.get('severity') == 'HIGH']
        
        if score >= 75:
            verdict = "Overall, the entity demonstrates robust financial health and high reporting integrity. "
        elif score >= 55:
            verdict = "The entity occupies a moderate risk bracket. While primary operations are stable, the localized discrepancies noted in the research section warrant close monitoring. "
        else:
            verdict = "The credit profile is under significant stress due to the accumulated high-severity contradictions and external signals. "
            
        if high_risks:
            concerns = f"The primary point of concern remains: {high_risks[0].get('message')}. "
        else:
            concerns = "No immediate disqualifying financial concerns were identified, though sectoral volatility remains a systemic factor. "
            
        return verdict + concerns

narrative_engine = NarrativeEngine()
