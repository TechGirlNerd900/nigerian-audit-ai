from pydantic import BaseModel
from typing import Dict, List, Any

class SamplingRequest(BaseModel):
    trial_balance: Dict[str, float]
    materiality: float
    risk_level: str = "medium"

class SamplingSuggestion(BaseModel):
    material_items: List[Dict[str, Any]]
    high_risk_samples: List[Dict[str, Any]]
    random_samples: List[Dict[str, Any]]

class SamplingResponse(BaseModel):
    success: bool
    suggestions: SamplingSuggestion

class WorkingPaperRequest(BaseModel):
    account_name: str
    transactions: List[Dict[str, Any]]

class WorkingPaperResponse(BaseModel):
    success: bool
    working_paper: List[Dict[str, Any]]
    title: str
