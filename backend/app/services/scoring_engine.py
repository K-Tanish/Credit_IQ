from typing import Dict, Any, List

class ScoringEngine:
    """
    Pillar 5 Service: Simulates a trained XGBoost PD model.
    Calculates Probability of Default (PD) and converts it to a CAMS Score.
    """

    def calculate_pd(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: Financial and compliance features.
        Output: PD percentage and feature importance (SHAP-style).
        """
        # Feature weights (simulated model coefficients)
        weights = {
            "turnover_variance": 0.4,
            "negative_news": 0.2,
            "sector_risk": 0.1,
            "document_integrity": 0.3
        }

        # Calculate raw logit
        logit = 0
        logit += features.get("turnover_variance", 0) * weights["turnover_variance"]
        logit += (1 if features.get("has_negative_news") else 0) * weights["negative_news"]
        logit += (0.1 if features.get("sector") == "infrastructure" else 0) * weights["sector_risk"]
        logit += (1 - features.get("docs_approved_pct", 1)) * weights["document_integrity"]

        # Convert to probability (Simplified Sigmoid)
        pd_val = min(max(logit, 0.02), 0.98) # Floor at 2% for ongoing business
        
        # Calculate CAMS Score (Inversely proportional to PD)
        cams_score = int(100 * (1 - pd_val))

        # Simulated SHAP values
        shap_values = {
            "Financial Variance": round(features.get("turnover_variance", 0) * weights["turnover_variance"] * -100, 1),
            "News Sentiment": -20.0 if features.get("has_negative_news") else 5.0,
            "Sector Benchmark": -5.0 if features.get("sector") == "infrastructure" else 2.0,
            "Data Quality": -10.0 if features.get("docs_approved_pct", 1) < 0.5 else 10.0
        }

        return {
            "pd_percentage": round(pd_val * 100, 2),
            "cams_score": cams_score,
            "shap_summary": shap_values
        }

ai_scoring_engine = ScoringEngine()
