from pydantic import BaseModel
from typing import Dict, List

class AccountMappingRequest(BaseModel):
    trial_balance: Dict[str, float]

class MappedAccount(BaseModel):
    audit_category: str
    ifrs_code: str
    balance: float

class AccountMappingResponse(BaseModel):
    success: bool
    mapped_accounts: Dict[str, MappedAccount]
    lead_schedule: List[Dict[str, any]]
