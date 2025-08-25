from pydantic import BaseModel
from typing import List, Dict

class AuditReportRequest(BaseModel):
    company_name: str
    opinion: str
    findings: List[str]

class AuditReportResponse(BaseModel):
    success: bool
    report: str

class ManagementLetterRequest(BaseModel):
    company_name: str
    deficiencies: List[Dict[str, str]]

class ManagementLetterResponse(BaseModel):
    success: bool
    letter: str
