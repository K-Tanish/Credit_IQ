import re
from typing import Dict, Any, List
import json

class DocumentExtractor:
    """
    Pillar 4: Handles sophisticated extraction of financial data 
    from raw text using template-based and semantic patterns.
    """

    def __init__(self):
        # Specific patterns for different document types
        self.templates = {
            "GST Return": {
                "turnover": [r"Total\s+Value\s+of\s+taxable\s+supplies.*?(\d[\d,.]*)", r"Outward\s+taxable\s+supplies.*?(\d[\d,.]*)"],
                "gst_paid": [r"Total\s+tax\s+payable.*?(\d[\d,.]*)", r"Integrated\s+Tax.*?(\d[\d,.]*)"],
                "period": [r"Return\s+Period.*?([A-Za-z]+\s+\d{4})", r"Month.*?([A-Za-z]+\s+\d{4})"]
            },
            "Bank Statement": {
                "total_credits": [r"Total\s+Credits.*?(\d[\d,.]*)", r"Total\s+Deposits.*?(\d[\d,.]*)"],
                "closing_balance": [r"Closing\s+Balance.*?(\d[\d,.]*)", r"Balance\s+as\s+on.*?(\d[\d,.]*)"],
                "account_number": [r"Account\s+No\.?.*?(\d{9,18})"]
            },
            "ITR Filing": {
                "gross_total_income": [r"Gross\s+Total\s+Income.*?(\d[\d,.]*)"],
                "tax_payable": [r"Total\s+Tax\s+Payable.*?(\d[\d,.]*)"]
            },
            "Shareholding Pattern": {
                "promoter_pledge_pct": [r"Shares\s+pledged\s+or\s+otherwise\s+encumbered.*?(\d[\d,.]*)", r"Pledge\s+.*?\s+(\d[\d,.]*)\s*%"]
            },
            "ALM Report": {
                "gap_1_to_30_days": [r"1\s*-\s*30\s*days.*?([-\d,.]+)"],
                "gap_31_to_90_days": [r"31\s*-\s*90\s*days.*?([-\d,.]+)"]
            }
        }

    def clean_num(self, val: str) -> float:
        if not val: return 0.0
        # Remove commas and other non-numeric chars except decimal
        cleaned = re.sub(r'[^\d.]', '', val)
        try:
            return float(cleaned)
        except:
            return 0.0

    def extract(self, doc_type: str, text: str) -> Dict[str, Any]:
        if not text:
            return {"error": "No text provided for extraction"}

        results = {"raw_values": {}}
        template = self.templates.get(doc_type, {})

        for field, patterns in template.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.I | re.S)
                if match:
                    val = match.group(1).strip()
                    # If it's a financial field, clean it
                    num_fields = [
                        "turnover", "gst_paid", "total_credits", "closing_balance", 
                        "gross_total_income", "tax_payable", "promoter_pledge_pct",
                        "gap_1_to_30_days", "gap_31_to_90_days"
                    ]
                    if field in num_fields:
                        results["raw_values"][field] = self.clean_num(val)
                    else:
                        results["raw_values"][field] = val
                    break # Stop at first match for this field
        
        # Add basic confidence score based on field coverage
        if template:
            found_count = len(results["raw_values"])
            expected_count = len(template)
            results["confidence"] = found_count / expected_count if expected_count > 0 else 0
        else:
            results["confidence"] = 0

        return results

extractor = DocumentExtractor()
