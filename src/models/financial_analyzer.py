import tensorflow as tf
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import logging
from ..utils.currency import format_ngn, validate_ngn_amount
from ..utils.nigerian_standards import NigerianFinancialRatios
from ..config.settings import settings

logger = logging.getLogger(__name__)

class FinancialAnalyzer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.nigerian_ratios = NigerianFinancialRatios()
        self.load_model()
    
    def load_model(self):
        """Load trained model from GCS or local storage"""
        try:
            model_path = f"gs://{settings.GCS_BUCKET}/models/financial_analyzer/{settings.MODEL_VERSION}"
            self.model = tf.keras.models.load_model(model_path)
            
            # Load scaler
            scaler_path = f"gs://{settings.GCS_BUCKET}/models/financial_analyzer/scaler.pkl"
            self.scaler = joblib.load(scaler_path)
            
            logger.info("Financial analyzer model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load model: {e}. Will train new model.")
            self.model = None
    
    def preprocess_trial_balance(self, trial_balance: Dict[str, float]) -> Dict:
        """Process and classify trial balance accounts"""
        
        # Validate Nigerian currency amounts
        for account, amount in trial_balance.items():
            if not validate_ngn_amount(amount):
                raise ValueError(f"Invalid NGN amount for {account}: {amount}")
        
        # Classify accounts according to Nigerian standards
        classification = {
            'current_assets': {},
            'non_current_assets': {},
            'current_liabilities': {},
            'non_current_liabilities': {},
            'equity': {},
            'revenue': {},
            'expenses': {},
            'other_comprehensive_income': {}
        }
        
        for account, amount in trial_balance.items():
            category = self._classify_account(account.lower())
            classification[category][account] = amount
        
        return classification
    
    def _classify_account(self, account_name: str) -> str:
        """Classify account based on Nigerian chart of accounts standards"""
        
        # Current Assets (1000-1999)
        current_asset_keywords = [
            'cash', 'bank', 'petty cash', 'call deposit', 'treasury bills',
            'accounts receivable', 'trade receivables', 'debtors',
            'inventory', 'stock', 'raw materials', 'work in progress',
            'prepaid expenses', 'advances', 'short term investments'
        ]
        
        # Non-Current Assets (1500-1999)
        non_current_asset_keywords = [
            'property', 'plant', 'equipment', 'ppe', 'building', 'land',
            'motor vehicle', 'furniture', 'computer', 'machinery',
            'intangible assets', 'goodwill', 'patents', 'software',
            'long term investments', 'investments in subsidiaries'
        ]
        
        # Current Liabilities (2000-2499)
        current_liability_keywords = [
            'accounts payable', 'trade payables', 'creditors',
            'accrued expenses', 'accruals', 'short term loans',
            'bank overdraft', 'vat payable', 'paye payable',
            'withholding tax', 'dividend payable', 'current portion'
        ]
        
        # Non-Current Liabilities (2500-2999)
        non_current_liability_keywords = [
            'long term loans', 'bonds payable', 'mortgage',
            'deferred tax liability', 'pension obligations',
            'long term provisions'
        ]
        
        # Revenue (4000-4999)
        revenue_keywords = [
            'sales', 'revenue', 'service revenue', 'interest income',
            'dividend income', 'rental income', 'other income',
            'gain on disposal'
        ]
        
        # Expenses (5000-5999)
        expense_keywords = [
            'cost of sales', 'cost of goods sold', 'salaries', 'wages',
            'rent expense', 'utilities', 'depreciation', 'amortization',
            'interest expense', 'bad debt', 'professional fees',
            'audit fees', 'insurance', 'repairs', 'maintenance'
        ]
        
        # Classification logic
        if any(keyword in account_name for keyword in current_asset_keywords):
            return 'current_assets'
        elif any(keyword in account_name for keyword in non_current_asset_keywords):
            return 'non_current_assets'
        elif any(keyword in account_name for keyword in current_liability_keywords):
            return 'current_liabilities'
        elif any(keyword in account_name for keyword in non_current_liability_keywords):
            return 'non_current_liabilities'
        elif any(keyword in account_name for keyword in revenue_keywords):
            return 'revenue'
        elif any(keyword in account_name for keyword in expense_keywords):
            return 'expenses'
        elif 'equity' in account_name or 'capital' in account_name or 'retained earnings' in account_name:
            return 'equity'
        else:
            return 'other_comprehensive_income'  # Default for unclassified
    
    def calculate_financial_ratios(self, classification: Dict) -> Dict[str, float]:
        """Calculate financial ratios according to Nigerian standards"""
        
        # Aggregate totals
        current_assets = sum(classification['current_assets'].values())
        non_current_assets = sum(classification['non_current_assets'].values())
        total_assets = current_assets + non_current_assets
        
        current_liabilities = sum(classification['current_liabilities'].values())
        non_current_liabilities = sum(classification['non_current_liabilities'].values())
        total_liabilities = current_liabilities + non_current_liabilities
        
        total_equity = sum(classification['equity'].values())
        total_revenue = sum(classification['revenue'].values())
        total_expenses = sum(classification['expenses'].values())
        
        net_income = total_revenue - total_expenses
        
        # Calculate ratios
        ratios = {}
        
        # Liquidity Ratios
        ratios['current_ratio'] = current_assets / current_liabilities if current_liabilities > 0 else 0
        
        # Quick assets = Current assets - Inventory
        inventory = sum(v for k, v in classification['current_assets'].items() 
                       if 'inventory' in k.lower() or 'stock' in k.lower())
        quick_assets = current_assets - inventory
        ratios['quick_ratio'] = quick_assets / current_liabilities if current_liabilities > 0 else 0
        
        # Leverage Ratios
        ratios['debt_to_equity'] = total_liabilities / total_equity if total_equity > 0 else 0
        ratios['debt_to_assets'] = total_liabilities / total_assets if total_assets > 0 else 0
        
        # Profitability Ratios
        ratios['gross_profit_margin'] = self._calculate_gross_profit_margin(classification)
        ratios['net_profit_margin'] = net_income / total_revenue if total_revenue > 0 else 0
        ratios['return_on_assets'] = net_income / total_assets if total_assets > 0 else 0
        ratios['return_on_equity'] = net_income / total_equity if total_equity > 0 else 0
        
        # Activity Ratios
        ratios['asset_turnover'] = total_revenue / total_assets if total_assets > 0 else 0
        
        return ratios
    
    def _calculate_gross_profit_margin(self, classification: Dict) -> float:
        """Calculate gross profit margin"""
        revenue = sum(classification['revenue'].values())
        cost_of_sales = sum(v for k, v in classification['expenses'].items() 
                           if 'cost of sales' in k.lower() or 'cost of goods sold' in k.lower())
        
        gross_profit = revenue - cost_of_sales
        return gross_profit / revenue if revenue > 0 else 0
    
    def assess_financial_health(self, ratios: Dict[str, float], 
                              company_type: str = "general") -> Dict:
        """Assess financial health using Nigerian industry benchmarks"""
        
        assessment = {
            'overall_score': 0,
            'risk_level': 'LOW',
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'compliance_flags': []
        }
        
        # Get Nigerian industry benchmarks
        benchmarks = self.nigerian_ratios.get_benchmarks(company_type)
        
        score = 0
        max_score = 0
        
        # Evaluate each ratio
        for ratio_name, ratio_value in ratios.items():
            if ratio_name in benchmarks:
                benchmark = benchmarks[ratio_name]
                ratio_score = self._score_ratio(ratio_name, ratio_value, benchmark)
                score += ratio_score
                max_score += 100
                
                # Add specific insights
                if ratio_score >= 80:
                    assessment['strengths'].append(f"Strong {ratio_name}: {ratio_value:.2f}")
                elif ratio_score <= 40:
                    assessment['weaknesses'].append(f"Weak {ratio_name}: {ratio_value:.2f}")
        
        # Calculate overall score
        assessment['overall_score'] = (score / max_score * 100) if max_score > 0 else 0
        
        # Determine risk level
        if assessment['overall_score'] >= 80:
            assessment['risk_level'] = 'LOW'
        elif assessment['overall_score'] >= 60:
            assessment['risk_level'] = 'MEDIUM'
        elif assessment['overall_score'] >= 40:
            assessment['risk_level'] = 'HIGH'
        else:
            assessment['risk_level'] = 'CRITICAL'
        
        # Generate recommendations
        assessment['recommendations'] = self._generate_recommendations(ratios, benchmarks)
        
        # Check Nigerian compliance flags
        assessment['compliance_flags'] = self._check_nigerian_compliance(ratios)
        
        return assessment
    
    def _score_ratio(self, ratio_name: str, value: float, benchmark: Dict) -> float:
        """Score individual ratio against benchmark"""
        
        if 'optimal_range' in benchmark:
            min_val, max_val = benchmark['optimal_range']
            if min_val <= value <= max_val:
                return 100
            elif value < min_val:
                return max(0, 100 - (min_val - value) / min_val * 100)
            else:
                return max(0, 100 - (value - max_val) / max_val * 100)
        
        elif 'target' in benchmark:
            target = benchmark['target']
            deviation = abs(value - target) / target if target != 0 else abs(value)
            return max(0, 100 - deviation * 100)
        
        return 50  # Default score for unknown benchmarks
    
    def _generate_recommendations(self, ratios: Dict[str, float], 
                                 benchmarks: Dict) -> List[str]:
        """Generate specific recommendations based on ratio analysis"""
        
        recommendations = []
        
        # Liquidity recommendations
        if ratios.get('current_ratio', 0) < 1.0:
            recommendations.append(
                "Improve liquidity by reducing current liabilities or increasing current assets"
            )
        elif ratios.get('current_ratio', 0) > 3.0:
            recommendations.append(
                "Consider investing excess current assets for better returns"
            )
        
        # Leverage recommendations
        if ratios.get('debt_to_equity', 0) > 1.0:
            recommendations.append(
                "High leverage detected. Consider debt reduction or equity financing"
            )
        
        # Profitability recommendations
        if ratios.get('net_profit_margin', 0) < 0.05:
            recommendations.append(
                "Low profitability. Review cost structure and pricing strategy"
            )
        
        return recommendations
    
    def _check_nigerian_compliance(self, ratios: Dict[str, float]) -> List[str]:
        """Check for Nigerian-specific compliance issues"""
        
        flags = []
        
        # CBN prudential guidelines for banks
        if ratios.get('current_ratio', 0) < 1.0:
            flags.append("Current ratio below CBN minimum requirement of 1.0")
        
        # FRC disclosure requirements
        if ratios.get('debt_to_equity', 0) > 2.0:
            flags.append("High leverage may require enhanced disclosure under FRC guidelines")
        
        return flags
    
    def analyze_financial_data(self, trial_balance: Dict[str, float], 
                             company_info: Dict = None) -> Dict:
        """Main analysis function"""
        
        try:
            # Preprocess data
            classification = self.preprocess_trial_balance(trial_balance)
            
            # Calculate ratios
            ratios = self.calculate_financial_ratios(classification)
            
            # Assess financial health
            company_type = company_info.get('type', 'general') if company_info else 'general'
            assessment = self.assess_financial_health(ratios, company_type)
            
            # Format amounts for Nigerian display
            formatted_classification = self._format_amounts(classification)
            
            return {
                'classification': formatted_classification,
                'ratios': ratios,
                'assessment': assessment,
                'summary': {
                    'total_assets': format_ngn(sum(classification['current_assets'].values()) + 
                                             sum(classification['non_current_assets'].values())),
                    'total_liabilities': format_ngn(sum(classification['current_liabilities'].values()) + 
                                                  sum(classification['non_current_liabilities'].values())),
                    'total_equity': format_ngn(sum(classification['equity'].values())),
                    'net_income': format_ngn(sum(classification['revenue'].values()) - 
                                           sum(classification['expenses'].values()))
                }
            }
            
        except Exception as e:
            logger.error(f"Error in financial analysis: {e}")
            raise
    
    def _format_amounts(self, classification: Dict) -> Dict:
        """Format amounts in Nigerian Naira"""
        formatted = {}
        for category, accounts in classification.items():
            formatted[category] = {
                account: format_ngn(amount) 
                for account, amount in accounts.items()
            }
        return formatted

# Export for use
__all__ = ['FinancialAnalyzer']