# docs/nigerian_regulations.md
# Nigerian Financial Regulations Guide

## Overview

This guide covers the key Nigerian financial regulations implemented in the audit AI system.

## Regulatory Bodies

### Financial Reporting Council (FRC)
- **Role**: Financial reporting standards and corporate governance
- **Website**: https://frcnigeria.gov.ng
- **Key Standards**: Nigerian IFRS, Corporate Governance Code

### Federal Inland Revenue Service (FIRS)  
- **Role**: Tax administration and collection
- **Website**: https://firs.gov.ng
- **Key Requirements**: TIN registration, tax filing, VAT compliance

### Corporate Affairs Commission (CAC)
- **Role**: Company registration and regulation
- **Website**: https://cac.gov.ng  
- **Key Requirements**: Company registration, annual returns

### Central Bank of Nigeria (CBN)
- **Role**: Banking regulation and monetary policy
- **Website**: https://cbn.gov.ng
- **Key Requirements**: Banking licenses, prudential guidelines

## Key Compliance Requirements

### FRC Compliance

#### Financial Statements Filing
- **Requirement**: Annual audited financial statements
- **Deadline**: 90 days after year-end
- **Penalty**: ₦500,000 - ₦2,000,000

#### IFRS Compliance  
- **Requirement**: Financial statements per Nigerian IFRS
- **Applicable to**: Public interest entities
- **Penalty**: ₦1,000,000 - ₦5,000,000

### FIRS Compliance

#### TIN Registration
- **Format**: 12-digit number
- **Requirement**: All business entities
- **Penalty**: ₦50,000 - ₦200,000

#### VAT Registration
- **Threshold**: ₦25,000,000 annual turnover
- **Rate**: 7.5% (proposed increase to 15%)
- **Deadline**: 30 days after threshold breach

#### Companies Income Tax (CIT)
- **Small companies** (≤₦25M): 0%
- **Medium companies** (₦25M-₦100M): 20%  
- **Large companies** (>₦100M): 30%

### CAMA Compliance

#### CAC Registration
- **Format**: RC123456 (companies), BN1234567 (business names)
- **Requirement**: All incorporated entities
- **Annual returns**: Within 42 days of AGM

### CBN Compliance (Banks)

#### Capital Adequacy
- **Minimum ratio**: 15%
- **Calculation**: Tier 1 + Tier 2 capital / Risk-weighted assets

#### Liquidity Ratio
- **Minimum ratio**: 30%
- **Calculation**: Liquid assets / Total deposits

## Nigerian IFRS Adaptations

### Mandatory Additional Disclosures
1. **Statement of Value Added**: Showing contribution to national economy
2. **Five-Year Financial Summary**: Trend analysis requirement
3. **Related Party Disclosures**: Enhanced Nigerian requirements

### Industry-Specific Requirements

#### Oil & Gas (Petroleum Industry Act 2021)
- Local content disclosures
- Environmental impact reporting
- Community development contributions

#### Banking (CBN Regulations)
- Prudential guideline compliance
- Risk management disclosures  
- Basel II/III implementation

#### Telecommunications (NCC Requirements)
- Infrastructure sharing disclosures
- Universal access contributions
- Quality of service metrics

## Tax Calculations

### Value Added Tax (VAT)
```python
# VAT Calculation
vat_rate = 0.075  # 7.5%
vat_amount = taxable_amount * vat_rate
total_amount = taxable_amount + vat_amount
```

### Withholding Tax (WHT)
```python
# WHT Rates
wht_rates = {
    'rent': 0.10,           # 10%
    'dividends': 0.10,      # 10%
    'interest': 0.10,       # 10%
    'professional_fees': 0.05,  # 5%
    'construction': 0.05    # 5%
}
```

### Companies Income Tax
```python
def calculate_cit(taxable_income, company_size):
    if company_size == 'small':
        return taxable_income * 0.0   # 0%
    elif company_size == 'medium':
        return taxable_income * 0.20  # 20%
    else:
        return taxable_income * 0.30  # 30%
```

## Compliance Scoring

### Scoring Methodology
- **Compliant**: 80-100 points
- **Partially Compliant**: 60-79 points  
- **Non-Compliant**: Below 60 points

### Penalty Assessment
- **Critical violations**: Immediate action required
- **High violations**: 30-day remediation
- **Medium violations**: 90-day remediation
- **Low violations**: Annual review

## Recent Updates (2024)

### FRC Updates
- IFRS Sustainability Standards roadmap (effective 2028)
- Enhanced audit quality indicators
- Updated corporate governance code

### FIRS Updates  
- New e-filing requirements
- Updated WHT rates for construction (5%)
- Enhanced TIN validation systems

### CBN Updates
- Increased banking capital requirements
- New foreign exchange regulations
- Enhanced cybersecurity requirements

## Resources

### Official Websites
- FRC Nigeria: https://frcnigeria.gov.ng
- FIRS: https://firs.gov.ng
- CAC: https://cac.gov.ng
- CBN: https://cbn.gov.ng

### Professional Bodies
- ICAN: https://ican.org.ng
- ANAN: https://anan.org.ng

### Legal Frameworks
- Companies and Allied Matters Act 2020
- Financial Reporting Council Act 2011
- Federal Inland Revenue Service Act 2019