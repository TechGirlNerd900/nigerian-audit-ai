# tests/test_integration.py
import pytest
import requests
import os
from src.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_financial_analysis():
    """Test financial analysis endpoint"""
    
    trial_balance = {
        "Cash and Bank": 5000000,
        "Accounts Receivable": 12000000,
        "Inventory": 8000000,
        "Property Plant Equipment": 25000000,
        "Accounts Payable": 4500000,
        "Long Term Loans": 15000000,
        "Share Capital": 20000000,
        "Sales Revenue": 30000000,
        "Cost of Sales": 18000000,
        "Operating Expenses": 8000000
    }
    
    response = client.post(
        "/api/v1/analyze/financial",
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"},
        json={
            "trial_balance": trial_balance,
            "company_info": {
                "type": "manufacturing",
                "size": "medium"
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "classification" in data["data"]
    assert "ratios" in data["data"]
    assert "assessment" in data["data"]

def test_compliance_check():
    """Test compliance checking endpoint"""
    
    response = client.post(
        "/api/v1/compliance/check",
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"},
        json={
            "company_data": {
                "cac_number": "RC123456",
                "tin_number": "123456789012",
                "business_type": "limited_liability"
            },
            "financial_data": {
                "annual_revenue": 50000000,
                "total_assets": 80000000
            },
            "regulations": ["FRC", "FIRS", "CAMA"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

# Run tests
if __name__ == "__main__":
    pytest.main([__file__])