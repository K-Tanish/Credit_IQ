import os
import json
from typing import List, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

class SWOTAgent:
    """
    Pillar 5 AI Agent: Uses LLMs to generate a professional SWOT analysis
    by synthesizing extracted document text, financial findings, and entity profiles.
    """

    def __init__(self):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        self.openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        
        # Initialize LLM
        self.llm = None
        if self.anthropic_key and "your_anthropic_api_key_here" not in self.anthropic_key:
            self.llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=self.anthropic_key)
        elif self.openai_key and "your_openai_api_key_here" not in self.openai_key:
            self.llm = ChatOpenAI(model="gpt-4o", openai_api_key=self.openai_key)

    async def generate_swot(self, entity_data: Dict[str, Any], findings: List[Dict[str, Any]], doc_texts: List[str]) -> Dict[str, List[str]]:
        """
        Generates structured SWOT points.
        """
        if not self.llm:
            return self._generate_smart_fallback_swot(entity_data, findings)

        # Truncate doc texts to fit context window
        context_text = "\n---\n".join([text[:2000] for text in doc_texts])
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are an expert Credit Analyst at a top-tier investment bank. "
                "Your task is to provide a structured SWOT analysis for a corporate entity based on provided "
                "financial data, cross-verification findings, and raw document excerpts. "
                "Output MUST be in JSON format with keys: strengths, weaknesses, opportunities, threats. "
                "Each value must be a list of concise, professional bullet points."
            )),
            HumanMessage(content=(
                f"Entity Profile: {json.dumps(entity_data)}\n\n"
                f"Financial Findings: {json.dumps(findings)}\n\n"
                f"Document Excerpts:\n{context_text}\n\n"
                "Please generate the SWOT analysis."
            ))
        ])

        try:
            response = await self.llm.ainvoke(prompt.format_messages())
            content = response.content
            # Basic JSON extraction if LLM adds markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception as e:
            # Fallback to smart rule-based SWOT if LLM fails
            return self._generate_smart_fallback_swot(entity_data, findings)

    def _generate_smart_fallback_swot(self, entity_data: Dict[str, Any], findings: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Enhanced rule-based SWOT generation when LLM is unavailable.
        """
        strengths = ["Verified business entity with valid GST/PAN registration."]
        weaknesses = []
        opportunities = ["Potential for credit limit expansion based on historical turnover."]
        threats = ["Sectoral volatility in " + entity_data.get('sector', 'General Manufacturing')]

        # Analyze findings
        for f in findings:
            if f['severity'] == "HIGH":
                weaknesses.append(f['message'])
            elif f['severity'] == "MEDIUM":
                if f['type'] == "WARNING":
                    threats.append(f['message'])
                else:
                    weaknesses.append(f['message'])
            
            if f['type'] == "CONFIRMATION":
                strengths.append(f['message'])

        if not weaknesses:
            weaknesses.append("No critical internal financial red flags identified in primary documents.")
        
        if entity_data.get('loan_amount') and float(str(entity_data.get('loan_amount')).replace(',', '')) > 10000000:
            opportunities.append("Scalable business model requiring high-quantum financing.")

        return {
            "strengths": strengths[:4],
            "weaknesses": weaknesses[:4],
            "opportunities": opportunities[:4],
            "threats": threats[:4]
        }

swot_agent = SWOTAgent()
