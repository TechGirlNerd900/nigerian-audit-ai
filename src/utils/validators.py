import re
from typing import Dict, List, Optional
import requests
from datetime import datetime

class NigerianValidator:
    """Validate Nigerian business identifiers and compliance data"""
    
    def __init__(self):
        self.validation_cache = {}
    
    def validate_cac_number(self, cac_number: str) -> Dict[str, any]:
        """Validate CAC registration number"""
        
        # Clean input
        cac_clean = str(cac_number).strip().upper()
        
        result = {
            'valid': False,
            'format_valid': False,
            'type': None,
            'number': cac_clean,
            'api_verified': False,
            'details': {}
        }
        
        # Validate format
        if re.match(r'^RC\d{6,7}$', cac_clean):
            result['format_valid'] = True
            result['type'] = 'company'
        elif re.match(r'^BN\d{7}$', cac_clean):
            result['format_valid'] = True
            result['type'] = 'business_name'
        else:
            result['format_valid'] = False
            return result
        
        # Try API verification (if available)
        try:
            api_result = self._verify_cac_api(cac_clean)
            result['api_verified'] = api_result.get('verified', False)
            result['details'] = api_result.get('details', {})
        except Exception:
            pass  # API verification failed, continue with format validation
        
        result['valid'] = result['format_valid']
        return result
    
    def validate_tin_number(self, tin: str) -> Dict[str, any]:
        """Validate Tax Identification Number"""
        
        tin_clean = re.sub(r'\D', '', str(tin))
        
        result = {
            'valid': False,
            'format_valid': False,
            'number': tin_clean,
            'api_verified': False,
            'firs_status': None
        }
        
        # TIN must be 12 digits
        if len(tin_clean) == 12 and tin_clean.isdigit():
            result['format_valid'] = True
            
            # Try FIRS API verification
            try:
                firs_result = self._verify_tin_firs(tin_clean)
                result['api_verified'] = firs_result.get('verified', False)
                result['firs_status'] = firs_result.get('status', 'unknown')
            except Exception:
                pass
        
        result['valid'] = result['format_valid']
        return result
    
    def validate_bank_account(self, account_number: str, bank_code: str) -> Dict[str, any]:
        """Validate Nigerian bank account"""
        
        account_clean = re.sub(r'\D', '', str(account_number))
        
        result = {
            'valid': False,
            'format_valid': False,
            'account_number': account_clean,
            'bank_code': bank_code,
            'account_name': None
        }
        
        # Nigerian account numbers are typically 10 digits
        if len(account_clean) == 10 and account_clean.isdigit():
            result['format_valid'] = True
            
            # Try account name verification via NIBSS
            try:
                name_result = self._verify_account_name(account_clean, bank_code)
                result['account_name'] = name_result.get('account_name')
                result['valid'] = name_result.get('verified', False)
            except Exception:
                result['valid'] = result['format_valid']
        
        return result
    
    def validate_phone_number(self, phone: str) -> Dict[str, any]:
        """Validate Nigerian phone number"""
        
        phone_clean = re.sub(r'\D', '', str(phone))
        
        result = {
            'valid': False,
            'format_valid': False,
            'number': phone_clean,
            'network': None,
            'formatted': None
        }
        
        # Nigerian mobile numbers
        if phone_clean.startswith('234') and len(phone_clean) == 13:
            # International format
            local_number = phone_clean[3:]
        elif phone_clean.startswith('0') and len(phone_clean) == 11:
            # Local format
            local_number = phone_clean[1:]
        elif len(phone_clean) == 10:
            # Without country/area code
            local_number = phone_clean
        else:
            return result
        
        # Validate network prefixes
        network_prefixes = {
            'MTN': ['803', '806', '813', '814', '816', '903', '906'],
            'Airtel': ['802', '808', '812', '901', '902', '904', '907'],
            'Glo': ['805', '807', '815', '811', '905'],
            '9mobile': ['809', '817', '818', '908', '909']
        }
        
        prefix = local_number[:3]
        for network, prefixes in network_prefixes.items():
            if prefix in prefixes:
                result['network'] = network
                result['format_valid'] = True
                result['valid'] = True
                result['formatted'] = f"+234{local_number}"
                break
        
        return result
    
    def _verify_cac_api(self, cac_number: str) -> Dict:
        """Verify CAC number via API"""
        # Placeholder for actual CAC API integration
        # Would integrate with CAC's official API when available
        return {
            'verified': False,
            'details': {
                'status': 'API not implemented',
                'last_checked': datetime.now().isoformat()
            }
        }
    
    def _verify_tin_firs(self, tin: str) -> Dict:
        """Verify TIN via FIRS API"""
        # Placeholder for FIRS API integration
        # Would integrate with FIRS ATRS API
        return {
            'verified': False,
            'status': 'API not implemented'
        }
    
    def _verify_account_name(self, account_number: str, bank_code: str) -> Dict:
        """Verify account name via NIBSS"""
        # Placeholder for NIBSS account verification
        return {
            'verified': False,
            'account_name': None
        }

# Export validator functions
validator = NigerianValidator()
validate_cac_number = validator.validate_cac_number
validate_tin_number = validator.validate_tin_number
validate_bank_account = validator.validate_bank_account
validate_phone_number = validator.validate_phone_number