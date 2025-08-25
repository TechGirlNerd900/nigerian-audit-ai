#src/config/sources.py

"""
This file centralizes the list of regulatory documents that can be downloaded directly.
These are primarily PDFs, direct HTML pages, or other files not requiring complex site navigation.
"""

GENERIC_REGULATORY_DOCUMENTS = [
    # Key Nigerian Legislation & Regulations
    {'name': 'CAMA 2020 Consolidated Act', 'url': 'https://www.cac.gov.ng/wp-content/uploads/2021/01/CAMA-2020.pdf'},
    {'name': 'FRCN Act 2011', 'url': 'https://www.frcnigeria.gov.ng/wp-content/uploads/2024/08/The-FRC-Act_merged.pdf'},
    {'name': 'FRCN Amendment Act 2023', 'url': 'https://frcnigeria.gov.ng/wp-content/uploads/2024/08/FRC-Amendment-Act.pdf'},
    {'name': 'Nigerian Code of Corporate Governance 2018', 'url': 'https://frcnigeria.gov.ng/wp-content/uploads/2024/08/NCCG-2018.pdf'},
    {'name': 'Finance Act 2023', 'url': 'https://www.firs.gov.ng/wp-content/uploads/2024/01/Finance-Act-2023-Official-Gazette.pdf'},
    {'name': 'Finance Act 2021', 'url': 'https://www.firs.gov.ng/wp-content/uploads/2022/04/FINANCE-ACT-2021-GAZETTED.pdf'},
    {'name': 'Finance Act 2020', 'url': 'https://www.firs.gov.ng/wp-content/uploads/2021/07/Finance-Act-2020.pdf'},
    {'name': 'Finance Act 2019', 'url': 'https://www.firs.gov.ng/wp-content/uploads/2021/07/Finance-Act-2019.pdf'},
    {'name': 'FIRS Transfer Pricing Regulations', 'url': 'https://www.firs.gov.ng/wp-content/uploads/2021/10/TP-REGULATION-GAZETTED-COPY.pdf'},
    {'name': 'CBN Prudential Guidelines for DMBs 2019', 'url': 'https://www.cbn.gov.ng/out/2019/fprd/exposure_dmbs%20%20august%202019.pdf'},
    {'name': 'CBN Guide to Charges by Banks and OFIs', 'url': 'https://www.cbn.gov.ng/out/2022/fgistd/guide%20to%20charges%20by%20banks%2c%20other%20financial%20and%20non-bank%20financial%20institutions.pdf'},

    # International Standards (IFRS & ISA) - Using Deloitte as an aggregator for direct PDF links
    {'name': 'IAS 1 Presentation of Financial Statements', 'url': 'https://www.iasplus.com/en/standards/ias/ias1'},
    {'name': 'IAS 2 Inventoriess', 'url': 'https://www.iasplus.com/en/standards/ias/ias2'},
    {'name': 'IAS 7 Statement of Cash Flows', 'url': 'https://www.iasplus.com/en/standards/ias/ias7'},
    {'name': 'IAS 8 Accounting Policies, Changes in Accounting Estimates and Errors', 'url': 'https://www.iasplus.com/en/standards/ias/ias8'},
    {'name': 'IAS 10 Events after the Reporting Period', 'url': 'https://www.iasplus.com/en/standards/ias/ias10'},
    {'name': 'IAS 12 Income Taxes', 'url': 'https://www.iasplus.com/en/standards/ias/ias12'},
    {'name': 'IAS 16 Property, Plant and Equipment', 'url': 'https://www.iasplus.com/en/standards/ias/ias16'},
    {'name': 'IAS 32 Financial Instruments Presentation', 'url': 'https://www.iasplus.com/en/standards/ias/ias32'},
    {'name': 'IAS 36 Impairment of Assets', 'url': 'https://www.iasplus.com/en/standards/ias/ias36'},
    {'name': 'IAS 37 Provisions, Contingent Liabilities and Contingent Assets', 'url': 'https://www.iasplus.com/en/standards/ias/ias37'},
    {'name': 'IFRS 1 First-time Adoption of International Financial Reporting Standards', 'url': 'https://www.iasplus.com/en/standards/ifrs/ifrs1'},
    {'name': 'IFRS 5 Non-current Assets Held for Sale and Discontinued Operations', 'url': 'https://www.iasplus.com/en/standards/ifrs/ifrs5'},
    {'name': 'IFRS 7 Financial Instruments Disclosures', 'url': 'https://www.iasplus.com/en/standards/ifrs/ifrs7'},
    {'name': 'IFRS 9 Financial Instruments', 'url': 'https://www.iasplus.com/en/standards/ifrs/ifrs9'},
    {'name': 'IFRS 13 Fair Value Measurement', 'url': 'https://www.iasplus.com/en/standards/ifrs/ifrs13'},
    {'name': 'IFRS 15 Revenue from Contracts with Customers', 'url': 'https://www.iasplus.com/en/standards/ifrs/ifrs15'},
    {'name': 'IFRS 16 Leases', 'url':'https://www.iasplus.com/en/standards/ifrs/ifrs16'},
    {'name': 'IFRS 17 Insurance Contracts', 'url': 'https://www.iasplus.com/en/standards/ifrs/ifrs17'},

    # Illustrative Statements & Templates
    {'name': 'Deloitte IFRS Illustrative Financial Statements 2023', 'url': 'https://www.iasplus.com/en/publications/global/ifrs-in-your-pocket/2023'},
    {'name': 'KPMG Illustrative Financial Statements IFRS 2023', 'url': 'https://kpmg.com/xx/en/home/insights/2023/10/illustrative-financial-statements-ifrs-2023.html'},
]    # Path: src/config/sources.py

"""
Centralized configuration for data sources used by the Nigerian Audit AI.
This includes official regulatory bodies, financial news, and economic data sources.
"""

class NigerianRegulatorySources:
    """
    Official Nigerian regulatory bodies and their key publications.
    """
    CAC_MAIN_PORTAL = "https://www.cac.gov.ng/"
    CAC_REGISTRATION_SEARCH = "https://search.cac.gov.ng/home" # Specific search portal
    FIRS_MAIN_PORTAL = "https://www.firs.gov.ng/"
    FIRS_TAX_LAWS = "https://www.firs.gov.ng/tax-laws/" # Section for tax laws
    FRCN_MAIN_PORTAL = "https://www.frcnigeria.gov.ng/"
    FRCN_STANDARDS_GUIDELINES = "https://www.frcnigeria.gov.ng/standards-guidelines/" # Financial reporting standards
    CBN_MAIN_PORTAL = "https://www.cbn.gov.ng/"
    CBN_REGULATIONS_GUIDELINES = "https://www.cbn.gov.ng/documents/regulations.asp" # Monetary policy, banking regulations
    NGX_MAIN_PORTAL = "https://www.ngxgroup.com/"
    NGX_LISTING_REQUIREMENTS = "https://www.ngxgroup.com/exchange/listing-rules/" # Rules for listed companies
    SEC_MAIN_PORTAL = "https://sec.gov.ng/"
    SEC_REGULATIONS_RULES = "https://sec.gov.ng/regulations-rules/" # Capital market regulations
    PENCOM_MAIN_PORTAL = "https://www.pencom.gov.ng/"
    PENCOM_GUIDELINES = "https://www.pencom.gov.ng/guidelines/" # Pension regulations
    NAICOM_MAIN_PORTAL = "https://naicom.gov.ng/"
    NAICOM_REGULATIONS = "https://naicom.gov.ng/regulations/" # Insurance regulations

class InternationalStandardsSources:
    """
    International accounting and auditing standards bodies.
    """
    IFRS_FOUNDATION = "https://www.ifrs.org/issued-standards/" # International Financial Reporting Standards
    IAASB = "https://www.iaasb.org/publications/international-standards-auditing-isas" # International Standards on Auditing
    AICPA = "https://www.aicpa.org/resources/auditing-and-attestation" # American Institute of CPAs (for general audit principles)
    PCAOB = "https://pcaobus.org/oversight/standards" # Public Company Accounting Oversight Board (US, but good for general audit practices)

class NigerianLegislationSources:
    """
    Key Nigerian legislation relevant to auditing and business.
    Note: Direct links to specific acts might require searching within government gazettes or legal databases.
    These are general portals.
    """
    LAWS_OF_THE_FEDERATION_PORTAL = "https://www.nigeria-law.org/" # Unofficial but comprehensive collection
    CAMA_2020_OVERVIEW = "https://www.pwc.com/ng/en/assets/pdf/companies-allied-matters-act-2020-overview.pdf" # PwC overview (example)
    FINANCE_ACTS_FIRS = FIRS_TAX_LAWS # Finance Acts are usually published by FIRS
    VAT_ACT_FIRS = FIRS_TAX_LAWS # VAT Act is part of tax laws

class FinancialNewsAndData:
    """
    Sources for financial news, market data, and economic indicators.
    """
    NBS_MAIN_PORTAL = "https://nigerianstat.gov.ng/" # National Bureau of Statistics (economic data)
    PROSHARE_NIGERIA = "https://www.proshareng.com/" # Leading financial information hub
    BUSINESSDAY_NEWSPAPER = "https://businessday.ng/" # Business news
    PREMIUM_TIMES_BUSINESS = "https://www.premiumtimesng.com/business" # Business news
    BLOOMBERG_AFRICA = "https://www.bloomberg.com/africa" # International perspective on African markets
    REUTERS_AFRICA = "https://www.reuters.com/markets/africa/" # International news on African markets

class OtherRelevantSources:
    """
    Miscellaneous but relevant sources for audit context.
    """
    EFCC_MAIN_PORTAL = "https://www.efcc.gov.ng/" # Economic and Financial Crimes Commission (anti-corruption)
    ICAEW_RESOURCES = "https://www.icaew.com/technical/audit-and-assurance" # Institute of Chartered Accountants in England and Wales (global best practices)
    ICAN_MAIN_PORTAL = "https://www.icanig.org/" # Institute of Chartered Accountants of Nigeria (local professional body)

# Example usage:
# print(NigerianRegulatorySources.CAC_MAIN_PORTAL)
# print(InternationalStandardsSources.IFRS_FOUNDATION)
