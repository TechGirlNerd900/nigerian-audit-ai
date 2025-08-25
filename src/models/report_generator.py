from typing import Dict, List
import google.generativeai as genai
from ..config.settings import settings

class ReportGenerator:
    """
    Generates draft audit reports and management letters using Google's Gemini model.
    """

    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_APPLICATION_CREDENTIALS)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_audit_report(self, company_name: str, opinion: str, findings: List[str]) -> str:
        """
        Generates a draft audit report using a generative AI model.
        """
        prompt = f"""
        As an expert AI audit assistant for a Nigerian accounting firm, generate a professional and compliant draft audit report.
        
        Company Name: {company_name}
        Audit Opinion: {opinion}
        
        Key Audit Findings:
        {self._format_list(findings)}

        Instructions:
        1.  Create a formal audit report.
        2.  The tone should be professional, objective, and compliant with International Standards on Auditing (ISAs).
        3.  Structure the report with standard sections: Opinion, Basis for Opinion, Key Audit Matters.
        4.  Incorporate the provided company name, opinion, and findings accurately.
        5.  Ensure the language reflects the specified audit opinion correctly.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def generate_management_letter(self, company_name: str, deficiencies: List[Dict[str, str]]) -> str:
        """
        Generates a draft management letter using a generative AI model.
        """
        prompt = f"""
        As an expert AI audit assistant for a Nigerian accounting firm, generate a professional and constructive draft management letter.

        Company Name: {company_name}

        Internal Control Deficiencies:
        {self._format_deficiencies(deficiencies)}

        Instructions:
        1.  Create a formal management letter addressed to the company's management.
        2.  The tone should be constructive and professional.
        3.  For each deficiency, clearly state the issue, its potential implication, and a concrete recommendation for improvement.
        4.  Structure the letter logically with an introduction, the detailed findings, and a concluding remark.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def _format_list(self, items: List[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    def _format_deficiencies(self, deficiencies: List[Dict[str, str]]) -> str:
        formatted = ""
        for item in deficiencies:
            formatted += f"- Deficiency: {item.get('deficiency', 'N/A')}\n"
            formatted += f"  Implication: {item.get('implication', 'N/A')}\n"
            formatted += f"  Recommendation: {item.get('recommendation', 'N/A')}\n\n"
        return formatted
