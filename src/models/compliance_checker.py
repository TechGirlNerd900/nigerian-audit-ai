import logging
from typing import Dict, List, Any
from datetime import datetime
from ..utils.nigerian_standards import NigerianTaxRates
from ..utils.validators import NigerianValidator
from ..schemas.compliance import ComplianceStatus, ViolationSeverity, ComplianceViolation

logger = logging.getLogger(__name__)

class ComplianceChecker:
    """Nigerian regulatory compliance checker"""
    
    def __init__(self):
        self.validator = NigerianValidator()
        self.tax_rates = NigerianTaxRates()
        
    def check_compliance(self, company_data: Dict, financial_data: Dict, regulations: List[str]) -> Dict:
        """Main compliance checking function"""
        
        results = {
            'overview': {
                'overall_status': ComplianceStatus.COMPLIANT,
                'overall_score': 100.0,
                'total_violations': 0,
                'critical_violations': 0,
                'regulations_checked': regulations,
                'last_updated': datetime.utcnow().isoformat()
            },
            'detailed_results': [],
            'recommendations': [],
            'action_items': []
        }
        
        for regulation in regulations:
            if regulation == 'FRC':
                result = self._check_frc_compliance(company_data, financial_data)
            elif regulation == 'FIRS':
                result = self._check_firs_compliance(company_data, financial_data)
            elif regulation == 'CAMA':
                result = self._check_cama_compliance(company_data, financial_data)
            elif regulation == 'CBN':
                result = self._check_cbn_compliance(company_data, financial_data)
            else:
                result = self._check_general_compliance(company_data, financial_data, regulation)
            
            results['detailed_results'].append(result)
            
            # Update overall metrics
            if result['violations']:
                results['overview']['total_violations'] += len(result['violations'])
                critical_count = len([v for v in result['violations'] if v['severity'] == ViolationSeverity.CRITICAL])
                results['overview']['critical_violations'] += critical_count
        
        # Calculate overall status and score
        total_violations = results['overview']['total_violations']
        critical_violations = results['overview']['critical_violations']
        
        if critical_violations > 0:
            results['overview']['overall_status'] = ComplianceStatus.NON_COMPLIANT
            results['overview']['overall_score'] = max(0, 40 - (critical_violations * 10))
        elif total_violations > 0:
            results['overview']['overall_status'] = ComplianceStatus.PARTIALLY_COMPLIANT
            results['overview']['overall_score'] = max(50, 90 - (total_violations * 5))
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results['detailed_results'])
        results['action_items'] = self._generate_action_items(results['detailed_results'])
        
        return results
    
    def _check_frc_compliance(self, company_data: Dict, financial_data: Dict) -> Dict:
        """Check Financial Reporting Council compliance"""
        
        violations = []
        requirements_met = []
        missing_requirements = []
        
        # Check if company is required to file with FRC
        annual_revenue = financial_data.get('annual_revenue', 0)
        is_public = company_data.get('is_public', False)
        
        if is_public or annual_revenue > 500_000_000:  # ₦500M threshold
            # Check financial statement filing
            if not financial_data.get('financial_statements_filed', False):
                violations.append({
                    'regulation': 'FRC',
                    'violation_type': 'Filing Requirement',
                    'description': 'Annual financial statements not filed with FRC',
                    'severity': ViolationSeverity.HIGH,
                    'recommendation': 'File audited financial statements within 90 days of year-end',
                    'penalty_range': '₦500,000 - ₦2,000,000',
                    'deadline': 'Within 90 days of financial year-end'
                })
                missing_requirements.append('Annual financial statements filing')
            else:
                requirements_met.append('Annual financial statements filed')
            
            # Check IFRS compliance
            if not financial_data.get('ifrs_compliant', True):
                violations.append({
                    'regulation': 'FRC',
                    'violation_type': 'IFRS Compliance',
                    'description': 'Financial statements not prepared in accordance with IFRS',
                    'severity': ViolationSeverity.CRITICAL,
                    'recommendation': 'Ensure financial statements comply with Nigerian IFRS',
                    'penalty_range': '₦1,000,000 - ₦5,000,000'
                })
                missing_requirements.append('IFRS compliance')
            else:
                requirements_met.append('IFRS compliance')
        
        # Calculate compliance score
        total_checks = len(requirements_met) + len(missing_requirements)
        score = (len(requirements_met) / total_checks * 100) if total_checks > 0 else 100
        
        # Determine status
        if violations:
            critical_violations = [v for v in violations if v['severity'] == ViolationSeverity.CRITICAL]
            status = ComplianceStatus.NON_COMPLIANT if critical_violations else ComplianceStatus.PARTIALLY_COMPLIANT
        else:
            status = ComplianceStatus.COMPLIANT
        
        return {
            'regulation': 'FRC',
            'status': status,
            'score': score,
            'violations': violations,
            'requirements_met': requirements_met,
            'missing_requirements': missing_requirements
        }
    
    def _check_firs_compliance(self, company_data: Dict, financial_data: Dict) -> Dict:
        """Check Federal Inland Revenue Service compliance"""
        
        violations = []
        requirements_met = []
        missing_requirements = []
        
        # Validate TIN
        tin_number = company_data.get('tin_number')
        if tin_number:
            tin_validation = self.validator.validate_tin_number(tin_number)
            if not tin_validation['format_valid']:
                violations.append({
                    'regulation': 'FIRS',
                    'violation_type': 'TIN Format',
                    'description': 'Invalid Tax Identification Number format',
                    'severity': ViolationSeverity.HIGH,
                    'recommendation': 'Obtain valid 12-digit TIN from FIRS',
                    'penalty_range': '₦50,000 - ₦200,000'
                })
                missing_requirements.append('Valid TIN')
            else:
                requirements_met.append('Valid TIN format')
        else:
            violations.append({
                'regulation': 'FIRS',
                'violation_type': 'TIN Missing',
                'description': 'Tax Identification Number not provided',
                'severity': ViolationSeverity.CRITICAL,
                'recommendation': 'Register for TIN with FIRS immediately'
            })
            missing_requirements.append('TIN registration')
        
        # Check VAT registration requirement
        annual_revenue = financial_data.get('annual_revenue', 0)
        if annual_revenue > self.tax_rates.VAT_THRESHOLD:
            if not financial_data.get('vat_registered', False):
                violations.append({
                    'regulation': 'FIRS',
                    'violation_type': 'VAT Registration',
                    'description': f'Company exceeds VAT threshold (₦{self.tax_rates.VAT_THRESHOLD:,}) but not registered for VAT',
                    'severity': ViolationSeverity.HIGH,
                    'recommendation': 'Register for VAT with FIRS within 30 days',
                    'penalty_range': '₦100,000 - ₦500,000'
                })
                missing_requirements.append('VAT registration')
            else:
                requirements_met.append('VAT registration')
        
        # Check tax filing compliance
        if not financial_data.get('tax_returns_filed', False):
            violations.append({
                'regulation': 'FIRS',
                'violation_type': 'Tax Filing',
                'description': 'Annual tax returns not filed',
                'severity': ViolationSeverity.CRITICAL,
                'recommendation': 'File annual tax returns before due date',
                'penalty_range': '₦25,000 + 10% of tax due',
                'deadline': 'Within 6 months of financial year-end'
            })
            missing_requirements.append('Tax returns filing')
        else:
            requirements_met.append('Tax returns filed')
        
        # Calculate score and status
        total_checks = len(requirements_met) + len(missing_requirements)
        score = (len(requirements_met) / total_checks * 100) if total_checks > 0 else 100
        
        if violations:
            critical_violations = [v for v in violations if v['severity'] == ViolationSeverity.CRITICAL]
            status = ComplianceStatus.NON_COMPLIANT if critical_violations else ComplianceStatus.PARTIALLY_COMPLIANT
        else:
            status = ComplianceStatus.COMPLIANT
        
        return {
            'regulation': 'FIRS',
            'status': status,
            'score': score,
            'violations': violations,
            'requirements_met': requirements_met,
            'missing_requirements': missing_requirements
        }
    
    def _check_cama_compliance(self, company_data: Dict, financial_data: Dict) -> Dict:
        """Check Companies and Allied Matters Act compliance"""
        
        violations = []
        requirements_met = []
        missing_requirements = []
        
        # Validate CAC number
        cac_number = company_data.get('cac_number')
        if cac_number:
            cac_validation = self.validator.validate_cac_number(cac_number)
            if not cac_validation['format_valid']:
                violations.append({
                    'regulation': 'CAMA',
                    'violation_type': 'CAC Registration',
                    'description': 'Invalid CAC registration number format',
                    'severity': ViolationSeverity.CRITICAL,
                    'recommendation': 'Ensure proper company registration with CAC'
                })
                missing_requirements.append('Valid CAC registration')
            else:
                requirements_met.append('Valid CAC registration')
        else:
            violations.append({
                'regulation': 'CAMA',
                'violation_type': 'CAC Missing',
                'description': 'CAC registration number not provided',
                'severity': ViolationSeverity.CRITICAL,
                'recommendation': 'Register company with Corporate Affairs Commission'
            })
            missing_requirements.append('CAC registration')
        
        # Check annual returns filing
        if not financial_data.get('annual_returns_filed', False):
            violations.append({
                'regulation': 'CAMA',
                'violation_type': 'Annual Returns',
                'description': 'Annual returns not filed with CAC',
                'severity': ViolationSeverity.MEDIUM,
                'recommendation': 'File annual returns with CAC',
                'penalty_range': '₦50,000 - ₦200,000',
                'deadline': 'Within 42 days of AGM'
            })
            missing_requirements.append('Annual returns filing')
        else:
            requirements_met.append('Annual returns filed')
        
        # Calculate score and status
        total_checks = len(requirements_met) + len(missing_requirements)
        score = (len(requirements_met) / total_checks * 100) if total_checks > 0 else 100
        
        if violations:
            critical_violations = [v for v in violations if v['severity'] == ViolationSeverity.CRITICAL]
            status = ComplianceStatus.NON_COMPLIANT if critical_violations else ComplianceStatus.PARTIALLY_COMPLIANT
        else:
            status = ComplianceStatus.COMPLIANT
        
        return {
            'regulation': 'CAMA',
            'status': status,
            'score': score,
            'violations': violations,
            'requirements_met': requirements_met,
            'missing_requirements': missing_requirements
        }
    
    def _check_cbn_compliance(self, company_data: Dict, financial_data: Dict) -> Dict:
        """Check Central Bank of Nigeria compliance (for banks and financial institutions)"""
        
        violations = []
        requirements_met = []
        missing_requirements = []
        
        business_type = company_data.get('business_type', '').lower()
        
        # Only applicable to banks and financial institutions
        if 'bank' in business_type or 'financial' in business_type:
            # Check capital adequacy
            capital_ratio = financial_data.get('capital_adequacy_ratio', 0)
            if capital_ratio < 0.15:  # 15% minimum
                violations.append({
                    'regulation': 'CBN',
                    'violation_type': 'Capital Adequacy',
                    'description': f'Capital adequacy ratio ({capital_ratio:.1%}) below CBN minimum of 15%',
                    'severity': ViolationSeverity.CRITICAL,
                    'recommendation': 'Increase capital to meet CBN requirements'
                })
                missing_requirements.append('Adequate capital ratio')
            else:
                requirements_met.append('Capital adequacy maintained')
            
            # Check liquidity ratio
            liquidity_ratio = financial_data.get('liquidity_ratio', 0)
            if liquidity_ratio < 0.30:  # 30% minimum
                violations.append({
                    'regulation': 'CBN',
                    'violation_type': 'Liquidity Ratio',
                    'description': f'Liquidity ratio ({liquidity_ratio:.1%}) below CBN minimum of 30%',
                    'severity': ViolationSeverity.HIGH,
                    'recommendation': 'Improve liquidity position'
                })
                missing_requirements.append('Adequate liquidity ratio')
            else:
                requirements_met.append('Liquidity requirements met')
        else:
            # Not applicable to non-financial institutions
            requirements_met.append('CBN regulations not applicable')
        
        # Calculate score and status
        total_checks = len(requirements_met) + len(missing_requirements)
        score = (len(requirements_met) / total_checks * 100) if total_checks > 0 else 100
        
        if violations:
            critical_violations = [v for v in violations if v['severity'] == ViolationSeverity.CRITICAL]
            status = ComplianceStatus.NON_COMPLIANT if critical_violations else ComplianceStatus.PARTIALLY_COMPLIANT
        else:
            status = ComplianceStatus.COMPLIANT
        
        return {
            'regulation': 'CBN',
            'status': status,
            'score': score,
            'violations': violations,
            'requirements_met': requirements_met,
            'missing_requirements': missing_requirements
        }
    
    def _check_general_compliance(self, company_data: Dict, financial_data: Dict, regulation: str) -> Dict:
        """Check general compliance for other regulations"""
        
        return {
            'regulation': regulation,
            'status': ComplianceStatus.REQUIRES_REVIEW,
            'score': 75.0,
            'violations': [],
            'requirements_met': ['Basic business registration'],
            'missing_requirements': [f'Specific {regulation} compliance assessment needed']
        }
    
    def _generate_recommendations(self, detailed_results: List[Dict]) -> List[str]:
        """Generate overall compliance recommendations"""
        
        recommendations = []
        
        # Count violations by severity
        all_violations = []
        for result in detailed_results:
            all_violations.extend(result['violations'])
        
        critical_violations = [v for v in all_violations if v['severity'] == ViolationSeverity.CRITICAL]
        high_violations = [v for v in all_violations if v['severity'] == ViolationSeverity.HIGH]
        
        if critical_violations:
            recommendations.append("Address critical compliance violations immediately to avoid penalties")
        
        if high_violations:
            recommendations.append("Develop a compliance action plan for high-priority violations")
        
        if len(all_violations) > 0:
            recommendations.append("Implement regular compliance monitoring and review processes")
        
        if not recommendations:
            recommendations.append("Maintain current compliance levels and monitor for regulatory changes")
        
        return recommendations
    
    def _generate_action_items(self, detailed_results: List[Dict]) -> List[str]:
        """Generate immediate action items"""
        
        action_items = []
        
        for result in detailed_results:
            for violation in result['violations']:
                if violation['severity'] in [ViolationSeverity.CRITICAL, ViolationSeverity.HIGH]:
                    action_items.append(f"{violation['regulation']}: {violation['recommendation']}")
        
        return action_items[:10]  # Limit to top 10 action items

