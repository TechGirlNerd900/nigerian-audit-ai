src/config/sources.py

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
]