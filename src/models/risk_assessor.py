import logging
from typing import Dict, List, Any
import numpy as np
from ..utils.nigerian_standards import NigerianFinancialRatios

logger = logging.getLogger(__name__)

class RiskAssessor:
    """Comprehensive risk assessment for Nigerian companies"""
    
    def __init__(self):
        self.benchmarks = NigerianFinancialRatios()
    
    def assess_risk(self, financial_data: Dict, company_info: Dict) -> Dict:
        """Main risk assessment function"""
        
        # Calculate individual risk components
        liquidity_risk = self._assess_liquidity_risk(financial_data)
        credit_risk = self._assess_credit_risk(financial_data)
        operational_risk = self._assess_operational_risk(financial_data, company_info)
        market_risk = self._assess_market_risk(financial_data, company_info)
        regulatory_risk = self._assess_regulatory_risk(company_info)
        
        # Calculate overall risk score
        risk_weights = {
            'liquidity': 0.25,
            'credit': 0.20,
            'operational': 0.25,
            'market': 0.20,
            'regulatory': 0.10
        }
        
        overall_score = (
            liquidity_risk['score'] * risk_weights['liquidity'] +
            credit_risk['score'] * risk_weights['credit'] +
            operational_risk['score'] * risk_weights['operational'] +
            market_risk['score'] * risk_weights['market'] +
            regulatory_risk['score'] * risk_weights['regulatory']
        )
        
        # Determine risk level
        if overall_score >= 80:
            risk_level = "LOW"
        elif overall_score >= 60:
            risk_level = "MEDIUM"
        elif overall_score >= 40:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        # Generate risk matrix
        risk_matrix = self._generate_risk_matrix([
            liquidity_risk, credit_risk, operational_risk, market_risk, regulatory_risk
        ])
        
        # Identify critical risks
        critical_risks = self._identify_critical_risks([
            liquidity_risk, credit_risk, operational_risk, market_risk, regulatory_risk
        ])
        
        # Generate mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(critical_risks)
        
        return {
            'overall_risk_score': overall_score,
            'risk_level': risk_level,
            'risk_components': {
                'liquidity_risk': liquidity_risk,
                'credit_risk': credit_risk,
                'operational_risk': operational_risk,
                'market_risk': market_risk,
                'regulatory_risk': regulatory_risk
            },
            'risk_matrix': risk_matrix,
            'critical_risks': critical_risks,
            'mitigation_strategies': mitigation_strategies,
            'recommendations': self._generate_risk_recommendations(risk_level, critical_risks)
        }
    
    def _assess_liquidity_risk(self, financial_data: Dict) -> Dict:
        """Assess liquidity risk"""
        
        current_ratio = financial_data.get('current_ratio', 0)
        quick_ratio = financial_data.get('quick_ratio', 0)
        cash_ratio = financial_data.get('cash_ratio', 0)
        
        # Score each ratio (0-100)
        current_score = self._score_ratio(current_ratio, 1.5, 2.5)
        quick_score = self._score_ratio(quick_ratio, 1.0, 1.5)
        cash_score = self._score_ratio(cash_ratio, 0.2, 0.5)
        
        # Overall liquidity score
        liquidity_score = (current_score + quick_score + cash_score) / 3
        
        # Identify specific risks
        risks = []
        if current_ratio < 1.0:
            risks.append("Current ratio below 1.0 indicates potential liquidity crisis")
        if quick_ratio < 0.8:
            risks.append("Quick ratio suggests difficulty meeting short-term obligations")
        if cash_ratio < 0.1:
            risks.append("Low cash ratio indicates poor cash management")
        
        return {
            'category': 'Liquidity Risk',
            'score': liquidity_score,
            'level': self._get_risk_level(liquidity_score),
            'factors': {
                'current_ratio': {'value': current_ratio, 'score': current_score},
                'quick_ratio': {'value': quick_ratio, 'score': quick_score},
                'cash_ratio': {'value': cash_ratio, 'score': cash_score}
            },
            'risks': risks,
            'impact': 'High' if liquidity_score < 50 else 'Medium' if liquidity_score < 70 else 'Low',
            'probability': 'High' if len(risks) >= 2 else 'Medium' if len(risks) == 1 else 'Low'
        }
    
    def _assess_credit_risk(self, financial_data: Dict) -> Dict:
        """Assess credit risk"""
        
        debt_to_equity = financial_data.get('debt_to_equity', 0)
        debt_to_assets = financial_data.get('debt_to_assets', 0)
        interest_coverage = financial_data.get('interest_coverage_ratio', 0)
        
        # Score each factor
        debt_equity_score = self._score_ratio(debt_to_equity, 0.3, 0.6, inverse=True)
        debt_assets_score = self._score_ratio(debt_to_assets, 0.2, 0.4, inverse=True)
        interest_score = self._score_ratio(interest_coverage, 2.5, 5.0)
        
        credit_score = (debt_equity_score + debt_assets_score + interest_score) / 3
        
        risks = []
        if debt_to_equity > 1.0:
            risks.append("High leverage increases financial risk")
        if debt_to_assets > 0.6:
            risks.append("High debt-to-assets ratio indicates over-leveraging")
        if interest_coverage < 2.0:
            risks.append("Low interest coverage suggests difficulty servicing debt")
        
        return {
            'category': 'Credit Risk',
            'score': credit_score,
            'level': self._get_risk_level(credit_score),
            'factors': {
                'debt_to_equity': {'value': debt_to_equity, 'score': debt_equity_score},
                'debt_to_assets': {'value': debt_to_assets, 'score': debt_assets_score},
                'interest_coverage': {'value': interest_coverage, 'score': interest_score}
            },
            'risks': risks,
            'impact': 'High' if credit_score < 50 else 'Medium' if credit_score < 70 else 'Low',
            'probability': 'High' if len(risks) >= 2 else 'Medium' if len(risks) == 1 else 'Low'
        }
    
    def _assess_operational_risk(self, financial_data: Dict, company_info: Dict) -> Dict:
        """Assess operational risk"""
        
        profit_margin = financial_data.get('net_profit_margin', 0)
        asset_turnover = financial_data.get('asset_turnover', 0)
        employee_productivity = financial_data.get('revenue_per_employee', 0)
        
        # Score operational metrics
        margin_score = self._score_ratio(profit_margin, 0.05, 0.15)
        turnover_score = self._score_ratio(asset_turnover, 0.5, 1.5)
        productivity_score = self._score_ratio(employee_productivity, 1_000_000, 5_000_000)  # ₦1M-5M per employee
        
        operational_score = (margin_score + turnover_score + productivity_score) / 3
        
        risks = []
        if profit_margin < 0:
            risks.append("Negative profit margins indicate operational inefficiency")
        if asset_turnover < 0.3:
            risks.append("Low asset turnover suggests poor asset utilization")
        
        # Industry-specific risks
        industry = company_info.get('industry', '').lower()
        if 'oil' in industry or 'gas' in industry:
            risks.append("Exposure to volatile oil prices")
        if 'manufacturing' in industry:
            risks.append("Supply chain and production risks")
        
        return {
            'category': 'Operational Risk',
            'score': operational_score,
            'level': self._get_risk_level(operational_score),
            'factors': {
                'profit_margin': {'value': profit_margin, 'score': margin_score},
                'asset_turnover': {'value': asset_turnover, 'score': turnover_score},
                'employee_productivity': {'value': employee_productivity, 'score': productivity_score}
            },
            'risks': risks,
            'impact': 'Medium',
            'probability': 'Medium' if len(risks) > 0 else 'Low'
        }
    
    def _assess_market_risk(self, financial_data: Dict, company_info: Dict) -> Dict:
        """Assess market risk"""
        
        # Basic market risk assessment
        revenue_growth = financial_data.get('revenue_growth', 0)
        market_concentration = financial_data.get('customer_concentration', 0.3)  # Default 30%
        
        growth_score = self._score_ratio(revenue_growth, -0.1, 0.1)  # -10% to +10% acceptable
        concentration_score = self._score_ratio(market_concentration, 0.2, 0.5, inverse=True)
        
        market_score = (growth_score + concentration_score) / 2
        
        risks = []
        if revenue_growth < -0.05:  # More than 5% decline
            risks.append("Declining revenue indicates market challenges")
        if market_concentration > 0.5:
            risks.append("High customer concentration increases market risk")
        
        # Nigerian market-specific risks
        risks.append("Exposure to Nigerian economic volatility")
        risks.append("Foreign exchange rate fluctuations (USD/NGN)")
        
        return {
            'category': 'Market Risk',
            'score': market_score,
            'level': self._get_risk_level(market_score),
            'factors': {
                'revenue_growth': {'value': revenue_growth, 'score': growth_score},
                'customer_concentration': {'value': market_concentration, 'score': concentration_score}
            },
            'risks': risks,
            'impact': 'High',  # Nigerian market volatility
            'probability': 'Medium'
        }
    
    def _assess_regulatory_risk(self, company_info: Dict) -> Dict:
        """Assess regulatory risk"""
        
        # Basic regulatory assessment
        is_public = company_info.get('is_public', False)
        industry = company_info.get('industry', '').lower()
        
        # Base score
        regulatory_score = 70  # Default medium risk
        
        risks = []
        
        # Industry-specific regulatory risks
        if 'bank' in industry or 'financial' in industry:
            regulatory_score -= 20
            risks.append("Subject to CBN prudential regulations")
            risks.append("Banking sector regulatory changes")
        
        if 'oil' in industry or 'gas' in industry:
            regulatory_score -= 15
            risks.append("Petroleum Industry Act compliance")
            risks.append("NNPC and DPR regulatory oversight")
        
        if 'telecom' in industry:
            regulatory_score -= 10
            risks.append("NCC regulatory requirements")
        
        if is_public:
            regulatory_score -= 10
            risks.append("SEC disclosure requirements")
            risks.append("NGX listing requirements")
        
        # General Nigerian regulatory risks
        risks.extend([
            "Changes in Nigerian tax laws",
            "FRC regulatory updates",
            "CAMA compliance requirements"
        ])
        
        return {
            'category': 'Regulatory Risk',
            'score': max(0, regulatory_score),
            'level': self._get_risk_level(max(0, regulatory_score)),
            'factors': {
                'industry_regulation': {'value': industry, 'score': regulatory_score},
                'public_company': {'value': is_public, 'score': 90 if not is_public else 70}
            },
            'risks': risks,
            'impact': 'Medium',
            'probability': 'High'  # Regulatory changes are common
        }
    
    def _score_ratio(self, value: float, min_good: float, max_good: float, inverse: bool = False) -> float:
        """Score a ratio against benchmarks (0-100)"""
        
        if inverse:
            # Lower values are better (e.g., debt ratios)
            if value <= min_good:
                return 100
            elif value >= max_good:
                return 0
            else:
                return 100 - ((value - min_good) / (max_good - min_good) * 100)
        else:
            # Higher values are better (e.g., profitability ratios)
            if value >= max_good:
                return 100
            elif value <= min_good:
                return 0
            else:
                return (value - min_good) / (max_good - min_good) * 100
    
    def _get_risk_level(self, score: float) -> str:
        """Convert score to risk level"""
        if score >= 80:
            return "LOW"
        elif score >= 60:
            return "MEDIUM"
        elif score >= 40:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _generate_risk_matrix(self, risk_components: List[Dict]) -> List[Dict]:
        """Generate risk matrix"""
        
        matrix = []
        for component in risk_components:
            matrix.append({
                'category': component['category'],
                'impact': component['impact'],
                'probability': component['probability'],
                'risk_level': component['level'],
                'score': component['score']
            })
        
        return sorted(matrix, key=lambda x: x['score'])
    
    def _identify_critical_risks(self, risk_components: List[Dict]) -> List[Dict]:
        """Identify critical risks requiring immediate attention"""
        
        critical_risks = []
        for component in risk_components:
            if component['level'] in ['CRITICAL', 'HIGH']:
                critical_risks.append({
                    'category': component['category'],
                    'level': component['level'],
                    'score': component['score'],
                    'key_risks': component['risks'][:3]  # Top 3 risks
                })
        
        return critical_risks
    
    def _generate_mitigation_strategies(self, critical_risks: List[Dict]) -> List[str]:
        """Generate risk mitigation strategies"""
        
        strategies = []
        
        for risk in critical_risks:
            category = risk['category']
            
            if 'Liquidity' in category:
                strategies.extend([
                    "Improve cash flow management and forecasting",
                    "Establish credit facilities for working capital",
                    "Optimize accounts receivable collection"
                ])
            
            elif 'Credit' in category:
                strategies.extend([
                    "Reduce debt levels through equity financing",
                    "Negotiate better debt terms with lenders",
                    "Improve debt service coverage ratios"
                ])
            
            elif 'Operational' in category:
                strategies.extend([
                    "Implement cost reduction initiatives",
                    "Improve operational efficiency and productivity",
                    "Diversify revenue streams"
                ])
            
            elif 'Market' in category:
                strategies.extend([
                    "Diversify customer base and markets",
                    "Hedge foreign exchange exposures",
                    "Develop market-responsive products"
                ])
            
            elif 'Regulatory' in category:
                strategies.extend([
                    "Establish compliance monitoring systems",
                    "Engage regulatory consultants",
                    "Stay updated on regulatory changes"
                ])
        
        return list(set(strategies))  # Remove duplicates
    
    def _generate_risk_recommendations(self, risk_level: str, critical_risks: List[Dict]) -> List[str]:
        """Generate overall risk management recommendations"""
        
        recommendations = []
        
        if risk_level == "CRITICAL":
            recommendations.append("Immediate risk mitigation actions required")
            recommendations.append("Consider engaging crisis management consultants")
        
        elif risk_level == "HIGH":
            recommendations.append("Develop comprehensive risk management plan")
            recommendations.append("Implement regular risk monitoring procedures")
        
        elif risk_level == "MEDIUM":
            recommendations.append("Maintain current risk controls and monitoring")
            recommendations.append("Prepare contingency plans for identified risks")
        
        else:  # LOW
            recommendations.append("Continue current risk management practices")
            recommendations.append("Monitor for emerging risks")
        
        if len(critical_risks) > 0:
            recommendations.append("Focus on critical risk areas identified")
        
        recommendations.append("Regular risk assessment updates recommended")
        
        return recommendations
