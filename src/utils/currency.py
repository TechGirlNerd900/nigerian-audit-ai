import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Union
import locale

class NigerianCurrency:
    """Handle Nigerian Naira currency operations"""
    
    NAIRA_SYMBOL = "₦"
    CURRENCY_CODE = "NGN"
    
    @staticmethod
    def format_ngn(amount: Union[float, int, Decimal]) -> str:
        """Format amount as Nigerian Naira"""
        try:
            # Convert to Decimal for precision
            decimal_amount = Decimal(str(amount))
            
            # Round to 2 decimal places
            rounded_amount = decimal_amount.quantize(
                Decimal('0.01'), 
                rounding=ROUND_HALF_UP
            )
            
            # Format with commas
            formatted = "{:,}".format(float(rounded_amount))
            
            return f"₦{formatted}"
            
        except (ValueError, TypeError):
            return "₦0.00"
    
    @staticmethod
    def parse_ngn(amount_str: str) -> float:
        """Parse NGN string to float"""
        try:
            # Remove currency symbols and whitespace
            cleaned = re.sub(r'[₦\s,]', '', str(amount_str))
            return float(cleaned)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def validate_ngn_amount(amount: Union[str, float, int]) -> bool:
        """Validate Nigerian Naira amount"""
        try:
            if isinstance(amount, str):
                parsed_amount = NigerianCurrency.parse_ngn(amount)
            else:
                parsed_amount = float(amount)
            
            # Check if amount is valid (positive and reasonable)
            return 0 <= parsed_amount <= 999_999_999_999  # 999 billion max
            
        except (ValueError, TypeError):
            return False

# Convenience functions
format_ngn = NigerianCurrency.format_ngn
parse_ngn = NigerianCurrency.parse_ngn
validate_ngn_amount = NigerianCurrency.validate_ngn_amount
