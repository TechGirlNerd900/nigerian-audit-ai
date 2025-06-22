from typing import Dict, List
from enum import Enum

class CompanySize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class IndustryType(Enum):
    MANUFACTURING = "manufacturing"
    BANKING = "banking"
    OIL_GAS = "oil_gas"
    TELECOMMUNICATIONS = "telecommunications"
    AGRICULTURE = "agriculture"
    RETAIL = "retail"
    SERVICES = "services"
    CONSTRUCTION = "construction"

class NigerianFinancialRatios:
    """Nigerian industry benchmarks and financial ratio standards"""
    
    def __init__(self):
        self.benchmarks = self._load_benchmarks()
    
    def _load_benchmarks(self) -> Dict:
        """Load Nigerian industry benchmarks"""
        
        return {
            'general': {
                'current_ratio': {'optimal_range': (1.5, 2.5), 'target': 2.0},
                'quick_ratio': {'optimal_range': (1.0, 1.5), 'target': 1.2},
                'debt_to_equity': {'optimal_range': (0.3, 0.6), 'target': 0.4},
                'debt_to_assets': {'optimal_range': (0.2, 0.4), 'target': 0.3},
                'gross_profit_margin': {'optimal_range': (0.2, 0.4), 'target': 0.3},
                'net_profit_margin': {'optimal_range': (0.05, 0.15), 'target': 0.1},
                'return_on_assets': {'optimal_range': (0.05, 0.15), 'target': 0.1},
                'return_on_equity': {'optimal_range': (0.12, 0.25), 'target': 0.18},
                'asset_turnover': {'optimal_range': (0.5, 1.5), 'target': 1.0}
            },
            'banking': {
                'current_ratio': {'optimal_range': (1.2, 1.8), 'target': 1.5},
                'debt_to_equity': {'optimal_range': (6.0, 12.0), 'target': 8.0},
                'return_on_assets': {'optimal_range': (0.015, 0.025), 'target': 0.02},
                'return_on_equity': {'optimal_range': (0.15, 0.25), 'target': 0.2},
                'capital_adequacy_ratio': {'optimal_range': (0.15, 0.20), 'target': 0.15}
            },
            'manufacturing': {
                'current_ratio': {'optimal_range': (1.5, 2.0), 'target': 1.75},
                'inventory_turnover': {'optimal_range': (4.0, 8.0), 'target': 6.0},
                'debt_to_equity': {'optimal_range': (0.4, 0.8), 'target': 0.6},
                'gross_profit_margin': {'optimal_range': (0.25, 0.35), 'target': 0.3},
                'asset_turnover': {'optimal_range': (0.8, 1.2), 'target': 1.0}
            },
            'oil_gas': {
                'current_ratio': {'optimal_range': (1.0, 1.5), 'target': 1.25},
                'debt_to_equity': {'optimal_range': (0.3, 0.7), 'target': 0.5},
                'return_on_assets': {'optimal_range': (0.08, 0.15), 'target': 0.12},
                'cash_ratio': {'optimal_range': (0.2, 0.4), 'target': 0.3}
            }
        }
    
    def get_benchmarks(self, industry: str) -> Dict:
        """Get benchmarks for specific industry"""
        return self.benchmarks.get(industry.lower(), self.benchmarks['general'])
    
    def get_company_size_thresholds(self) -> Dict:
        """Get Nigerian company size classification thresholds"""
        return {
            'small': {
                'annual_revenue': 25_000_000,  # ₦25M
                'total_assets': 50_000_000,    # ₦50M
                'employees': 50
            },
            'medium': {
                'annual_revenue': 500_000_000,  # ₦500M
                'total_assets': 1_000_000_000,  # ₦1B
                'employees': 300
            },
            'large': {
                'annual_revenue': float('inf'),
                'total_assets': float('inf'),
                'employees': float('inf')
            }
        }
    
    def classify_company_size(self, annual_revenue: float, 
                            total_assets: float, 
                            employee_count: int) -> str:
        """Classify company size based on Nigerian standards"""
        
        thresholds = self.get_company_size_thresholds()
        
        if (annual_revenue <= thresholds['small']['annual_revenue'] and
            total_assets <= thresholds['small']['total_assets'] and
            employee_count <= thresholds['small']['employees']):
            return 'small'
        
        elif (annual_revenue <= thresholds['medium']['annual_revenue'] and
              total_assets <= thresholds['medium']['total_assets'] and
              employee_count <= thresholds['medium']['employees']):
            return 'medium'
        
        else:
            return 'large'

class NigerianTaxRates:
    """Current Nigerian tax rates and calculations"""
    
    VAT_RATE = 0.075  # 7.5%
    VAT_THRESHOLD = 25_000_000  # ₦25M annual turnover
    
    # Companies Income Tax
    CIT_RATES = {
        'small': 0.0,   # 0% for small companies
        'medium': 0.20,  # 20% for medium companies  
        'large': 0.30    # 30% for large companies
    }
    
    # Withholding Tax Rates
    WHT_RATES = {
        'rent': 0.10,           # 10%
        'dividends': 0.10,      # 10%
        'interest': 0.10,       # 10%
        'royalties': 0.10,      # 10%
        'professional_fees': 0.05,  # 5%
        'construction': 0.05,   # 5%
        'consultancy': 0.05,    # 5%
        'commission': 0.05      # 5%
    }
    
    @classmethod
    def calculate_vat(cls, amount: float, vat_inclusive: bool = False) -> Dict:
        """Calculate VAT on amount"""
        
        if vat_inclusive:
            # Extract VAT from inclusive amount
            vat_amount = amount * cls.VAT_RATE / (1 + cls.VAT_RATE)
            net_amount = amount - vat_amount
        else:
            # Add VAT to exclusive amount
            vat_amount = amount * cls.VAT_RATE
            net_amount = amount
            amount = net_amount + vat_amount
        
        return {
            'net_amount': net_amount,
            'vat_amount': vat_amount,
            'gross_amount': amount,
            'vat_rate': cls.VAT_RATE
        }
    
    @classmethod
    def calculate_cit(cls, taxable_income: float, company_size: str) -> Dict:
        """Calculate Companies Income Tax"""
        
        rate = cls.CIT_RATES.get(company_size.lower(), cls.CIT_RATES['large'])
        tax_amount = taxable_income * rate
        
        return {
            'taxable_income': taxable_income,
            'tax_rate': rate,
            'tax_amount': tax_amount,
            'after_tax_income': taxable_income - tax_amount
        }
    
    @classmethod
    def calculate_wht(cls, amount: float, wht_type: str) -> Dict:
        """Calculate Withholding Tax"""
        
        rate = cls.WHT_RATES.get(wht_type.lower(), 0.05)  # Default 5%
        wht_amount = amount * rate
        net_amount = amount - wht_amount
        
        return {
            'gross_amount': amount,
            'wht_rate': rate,
            'wht_amount': wht_amount,
            'net_amount': net_amount
        }