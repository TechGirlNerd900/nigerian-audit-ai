import logging
import re
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
from datetime import datetime
from ..utils.validators import NigerianValidator

logger = logging.getLogger(__name__)

class EnhancedNigerianValidator(NigerianValidator):
    """Enhanced Nigerian validator with ML-powered validation and API integrations"""
    
    def __init__(self):
        super().__init__()
        self.api_cache = {}
        self.validation_patterns = self._load_validation_patterns()
        self.ml_models = {}
    
    def _load_validation_patterns(self) -> Dict:
        """Load Nigerian-specific validation patterns"""
        
        return {
            'cac_patterns': {
                'company': r'^RC\d{6,7}$',
                'business_name': r'^BN\d{7}$',
                'incorporated_trustees': r'^IT\d{6}$',
                'limited_liability_partnership': r'^LLP\d{4}$'
            },
            'tin_pattern': r'^\d{12}$',
            'bank_patterns': {
                'account_number': r'^\d{10}$',
                'sort_code': r'^\d{6}$',
                'bvn': r'^\d{11}$'
            },
            'phone_patterns': {
                'mobile': r'^(\+234|0)[789]\d{9}$',
                'landline': r'^(\+234|0)[1-9]\d{7,8}$'
            },
            'address_patterns': {
                'postal_code': r'^\d{6}$',
                'state_codes': [
                    'AB', 'AD', 'AK', 'AN', 'BA', 'BY', 'BE', 'BO', 'CR', 'DE',
                    'EB', 'ED', 'EK', 'EN', 'FC', 'GO', 'IM', 'JI', 'KD', 'KN',
                    'KT', 'KE', 'KO', 'KW', 'LA', 'NA', 'NI', 'OG', 'ON', 'OS',
                    'OY', 'PL', 'RI', 'SO', 'TA', 'YO', 'ZA'
                ]
            }
        }
    
    async def comprehensive_company_validation(self, company_data: Dict) -> Dict:
        """Comprehensive validation of Nigerian company data"""
        
        validation_result = {
            'overall_valid': True,
            'confidence_score': 0.0,
            'validations': {},
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
        
        # CAC validation
        if 'cac_number' in company_data:
            cac_result = await self._validate_cac_comprehensive(company_data['cac_number'])
            validation_result['validations']['cac'] = cac_result
            if not cac_result['valid']:
                validation_result['overall_valid'] = False
                validation_result['errors'].append("Invalid CAC registration number")
        
        # TIN validation
        if 'tin_number' in company_data:
            tin_result = await self._validate_tin_comprehensive(company_data['tin_number'])
            validation_result['validations']['tin'] = tin_result
            if not tin_result['valid']:
                validation_result['overall_valid'] = False
                validation_result['errors'].append("Invalid Tax Identification Number")
        
        # Business address validation
        if 'address' in company_data:
            address_result = self._validate_nigerian_address(company_data['address'])
            validation_result['validations']['address'] = address_result
            if not address_result['valid']:
                validation_result['warnings'].append("Address format may be incorrect")
        
        # Contact information validation
        if 'phone' in company_data:
            phone_result = self.validate_phone_number(company_data['phone'])
            validation_result['validations']['phone'] = phone_result
            if not phone_result['valid']:
                validation_result['errors'].append("Invalid phone number format")
        
        if 'email' in company_data:
            email_result = self._validate_email(company_data['email'])
            validation_result['validations']['email'] = email_result
            if not email_result['valid']:
                validation_result['errors'].append("Invalid email format")
        
        # Business type validation
        if 'business_type' in company_data:
            business_type_result = self._validate_business_type(
                company_data['business_type'], 
                company_data.get('cac_number', '')
            )
            validation_result['validations']['business_type'] = business_type_result
            if not business_type_result['valid']:
                validation_result['warnings'].append("Business type may not match CAC registration")
        
        # Industry sector validation
        if 'industry' in company_data:
            industry_result = self._validate_industry_sector(company_data['industry'])
            validation_result['validations']['industry'] = industry_result
        
        # Calculate confidence score
        validation_result['confidence_score'] = self._calculate_confidence_score(validation_result)
        
        # Generate recommendations
        validation_result['recommendations'] = self._generate_validation_recommendations(validation_result)
        
        return validation_result
    
    async def _validate_cac_comprehensive(self, cac_number: str) -> Dict:
        """Comprehensive CAC validation with API verification"""
        
        # Basic format validation
        basic_result = self.validate_cac_number(cac_number)
        
        # Enhanced validation
        enhanced_result = {
            **basic_result,
            'enhanced_checks': {
                'format_validation': basic_result['format_valid'],
                'api_verification': False,
                'business_status': 'unknown',
                'registration_date': None,
                'company_details': {},
                'directors': [],
                'share_capital': None
            }
        }
        
        if basic_result['format_valid']:
            # Try CAC API verification
            try:
                api_result = await self._query_cac_api(cac_number)
                enhanced_result['enhanced_checks'].update(api_result)
                enhanced_result['api_verified'] = api_result.get('verified', False)
            except Exception as e:
                logger.warning(f"CAC API verification failed: {e}")
        
        return enhanced_result
    
    async def _validate_tin_comprehensive(self, tin_number: str) -> Dict:
        """Comprehensive TIN validation with FIRS API"""
        
        # Basic format validation
        basic_result = self.validate_tin_number(tin_number)
        
        # Enhanced validation
        enhanced_result = {
            **basic_result,
            'enhanced_checks': {
                'format_validation': basic_result['format_valid'],
                'firs_verification': False,
                'tax_status': 'unknown',
                'registration_date': None,
                'taxpayer_type': None,
                'tax_office': None,
                'compliance_status': 'unknown'
            }
        }
        
        if basic_result['format_valid']:
            # Try FIRS API verification
            try:
                firs_result = await self._query_firs_api(tin_number)
                enhanced_result['enhanced_checks'].update(firs_result)
                enhanced_result['api_verified'] = firs_result.get('verified', False)
            except Exception as e:
                logger.warning(f"FIRS API verification failed: {e}")
        
        return enhanced_result
    
    def _validate_nigerian_address(self, address: str) -> Dict:
        """Validate Nigerian address format"""
        
        result = {
            'valid': False,
            'components': {},
            'formatted_address': None,
            'warnings': []
        }
        
        # Basic address validation
        if not address or len(address.strip()) < 10:
            result['warnings'].append("Address appears to be too short")
            return result
        
        # Look for Nigerian state names/codes
        nigerian_states = [
            'Lagos', 'Abuja', 'Kano', 'Ibadan', 'Port Harcourt', 'Benin City',
            'Maiduguri', 'Zaria', 'Aba', 'Jos', 'Ilorin', 'Oyo', 'Enugu',
            'Kaduna', 'Kumo', 'Ikeja', 'Yenagoa', 'Calabar', 'Uyo', 'Akure',
            'Bauchi', 'Sokoto', 'Gombe', 'Abeokuta', 'Awka', 'Asaba', 'Lokoja',
            'Yola', 'Jalingo', 'Lafia', 'Makurdi', 'Minna', 'Birnin Kebbi',
            'Dutse', 'Gusau', 'Damaturu', 'Owerri', 'Umuahia'
        ]
        
        state_found = False
        for state in nigerian_states:
            if state.lower() in address.lower():
                result['components']['state'] = state
                state_found = True
                break
        
        if not state_found:
            result['warnings'].append("No recognizable Nigerian state found in address")
        
        # Look for postal code
        postal_match = re.search(r'\b\d{6}\b', address)
        if postal_match:
            result['components']['postal_code'] = postal_match.group()
        else:
            result['warnings'].append("No postal code found")
        
        result['valid'] = state_found and len(result['warnings']) == 0
        result['formatted_address'] = address.strip()
        
        return result
    
    def _validate_email(self, email: str) -> Dict:
        """Validate email address"""
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        return {
            'valid': bool(re.match(email_pattern, email)),
            'format_valid': bool(re.match(email_pattern, email)),
            'domain': email.split('@')[1] if '@' in email else None,
            'is_corporate': self._is_corporate_email(email)
        }
    
    def _is_corporate_email(self, email: str) -> bool:
        """Check if email appears to be corporate"""
        
        if '@' not in email:
            return False
        
        domain = email.split('@')[1].lower()
        
        # Common personal email providers
        personal_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'yahoo.co.uk', 'aol.com', 'icloud.com'
        ]
        
        return domain not in personal_domains
    
    def _validate_business_type(self, business_type: str, cac_number: str) -> Dict:
        """Validate business type matches CAC registration"""
        
        valid_business_types = [
            'Private Limited Company',
            'Public Limited Company',
            'Limited by Guarantee',
            'Business Name',
            'Incorporated Trustees',
            'Limited Liability Partnership',
            'Sole Proprietorship'
        ]
        
        result = {
            'valid': business_type in valid_business_types,
            'normalized_type': business_type,
            'matches_cac': True,
            'warnings': []
        }
        
        # Check if business type matches CAC number pattern
        if cac_number:
            if cac_number.startswith('RC') and 'Limited Company' not in business_type:
                result['matches_cac'] = False
                result['warnings'].append("Business type may not match CAC registration pattern")
            elif cac_number.startswith('BN') and business_type != 'Business Name':
                result['matches_cac'] = False
                result['warnings'].append("Business type should be 'Business Name' for BN registration")
        
        return result
    
    def _validate_industry_sector(self, industry: str) -> Dict:
        """Validate industry sector classification"""
        
        nigerian_industries = [
            'Agriculture', 'Mining', 'Manufacturing', 'Construction',
            'Transportation', 'Communication', 'Finance and Insurance',
            'Real Estate', 'Professional Services', 'Education',
            'Healthcare', 'Entertainment', 'Oil and Gas', 'Banking',
            'Telecommunications', 'Information Technology', 'Retail',
            'Hospitality', 'Aviation', 'Maritime', 'Power', 'Water'
        ]
        
        # Fuzzy matching for industry
        industry_lower = industry.lower()
        matched_industry = None
        
        for standard_industry in nigerian_industries:
            if industry_lower in standard_industry.lower() or standard_industry.lower() in industry_lower:
                matched_industry = standard_industry
                break
        
        return {
            'valid': matched_industry is not None,
            'standardized_industry': matched_industry,
            'input_industry': industry,
            'suggestions': nigerian_industries if not matched_industry else []
        }
    
    async def _query_cac_api(self, cac_number: str) -> Dict:
        """Query CAC API for company details"""
        
        # Placeholder for actual CAC API integration
        # In production, this would make actual API calls to CAC
        
        return {
            'verified': False,
            'business_status': 'unknown',
            'registration_date': None,
            'company_details': {},
            'error': 'CAC API integration not yet available'
        }
    
    async def _query_firs_api(self, tin_number: str) -> Dict:
        """Query FIRS API for tax details"""
        
        # Placeholder for actual FIRS API integration
        # In production, this would make actual API calls to FIRS
        
        return {
            'verified': False,
            'tax_status': 'unknown',
            'compliance_status': 'unknown',
            'error': 'FIRS API integration not yet available'
        }
    
    def _calculate_confidence_score(self, validation_result: Dict) -> float:
        """Calculate overall confidence score for validation"""
        
        validations = validation_result['validations']
        total_checks = len(validations)
        
        if total_checks == 0:
            return 0.0
        
        valid_checks = sum(1 for v in validations.values() if v.get('valid', False))
        api_verified_checks = sum(1 for v in validations.values() if v.get('api_verified', False))
        
        base_score = (valid_checks / total_checks) * 100
        
        # Bonus for API verification
        api_bonus = (api_verified_checks / total_checks) * 10
        
        # Penalty for errors
        error_penalty = len(validation_result['errors']) * 5
        
        # Penalty for warnings
        warning_penalty = len(validation_result['warnings']) * 2
        
        confidence_score = base_score + api_bonus - error_penalty - warning_penalty
        
        return max(0.0, min(100.0, confidence_score))
    
    def _generate_validation_recommendations(self, validation_result: Dict) -> List[str]:
        """Generate recommendations based on validation results"""
        
        recommendations = []
        
        if validation_result['errors']:
            recommendations.append("Address critical validation errors before proceeding")
        
        if validation_result['warnings']:
            recommendations.append("Review and resolve validation warnings")
        
        # Specific recommendations based on failed validations
        validations = validation_result['validations']
        
        if 'cac' in validations and not validations['cac']['valid']:
            recommendations.append("Verify CAC registration number with Corporate Affairs Commission")
        
        if 'tin' in validations and not validations['tin']['valid']:
            recommendations.append("Obtain valid Tax Identification Number from FIRS")
        
        if 'address' in validations and not validations['address']['valid']:
            recommendations.append("Provide complete Nigerian address including state and postal code")
        
        if validation_result['confidence_score'] < 70:
            recommendations.append("Consider additional document verification for low confidence score")
        
        return recommendations
    
    async def validate_financial_data_integrity(self, financial_data: Dict) -> Dict:
        """Validate integrity of financial data"""
        
        result = {
            'valid': True,
            'checks': {},
            'anomalies': [],
            'warnings': []
        }
        
        # Check for basic accounting equation
        if all(key in financial_data for key in ['total_assets', 'total_liabilities', 'total_equity']):
            assets = financial_data['total_assets']
            liabilities = financial_data['total_liabilities']
            equity = financial_data['total_equity']
            
            balance_check = abs(assets - (liabilities + equity))
            tolerance = assets * 0.01  # 1% tolerance
            
            result['checks']['accounting_equation'] = {
                'valid': balance_check <= tolerance,
                'difference': balance_check,
                'tolerance': tolerance
            }
            
            if balance_check > tolerance:
                result['valid'] = False
                result['anomalies'].append(f"Accounting equation imbalance: {balance_check:,.2f}")
        
        # Check for negative values where inappropriate
        negative_checks = ['total_assets', 'revenue', 'cash']
        for field in negative_checks:
            if field in financial_data and financial_data[field] < 0:
                result['anomalies'].append(f"Negative value for {field}: {financial_data[field]:,.2f}")
                result['valid'] = False
        
        # Check for unrealistic ratios
        if 'revenue' in financial_data and 'total_assets' in financial_data:
            if financial_data['total_assets'] > 0:
                asset_turnover = financial_data['revenue'] / financial_data['total_assets']
                if asset_turnover > 10:  # Unrealistically high
                    result['warnings'].append(f"Unusually high asset turnover: {asset_turnover:.2f}")
                elif asset_turnover < 0.01:  # Unrealistically low
                    result['warnings'].append(f"Unusually low asset turnover: {asset_turnover:.2f}")
        
        return result