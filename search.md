Publicly Available Nigerian Datasets for AI-Driven Financial and Audit Automation: A Comprehensive Guide
Executive Summary
This report provides a comprehensive overview of publicly available, Nigerian-specific datasets essential for developing AI applications in financial analysis and auditing. While macroeconomic and regulatory textual data are relatively accessible from official government and professional body websites, granular financial transaction data and detailed audit working papers remain largely unavailable due to privacy and proprietary concerns. Key sources include the Central Bank of Nigeria (CBN), National Bureau of Statistics (NBS), Nigerian Exchange Group (NGX), Federal Inland Revenue Service (FIRS), Corporate Affairs Commission (CAC), and professional bodies like ICAN and ANAN. The emergence of Open Banking Nigeria offers a promising future for consented access to granular financial data. For critical data gaps, particularly in financial transactions and detailed audit processes, synthetic data generation is identified as a vital strategy for AI model training. AI developers should prioritize official government portals for reliable aggregated data and regulatory texts, actively monitor Open Banking developments, and strategically employ synthetic data generation to overcome limitations in granular, sensitive financial and audit information.

1. Introduction: The Data Landscape for AI in Nigerian Finance and Audit
The application of Artificial Intelligence (AI) in financial analysis and auditing holds immense potential for enhancing efficiency, accuracy, and insight generation across the Nigerian financial landscape. AI can automate routine tasks such as data entry and reconciliation, identify anomalies indicative of fraud or error, predict financial trends, and improve compliance processes by rapidly analyzing vast quantities of regulatory information. This transformative potential is, however, heavily reliant on access to high-quality, relevant, and sufficiently granular data.

In the Nigerian context, acquiring such data presents unique challenges. These challenges primarily stem from stringent data privacy regulations, the proprietary nature of much financial information held by private entities, and the relatively nascent stage of widespread AI adoption and data sharing initiatives in certain sectors. Consequently, while some aggregated macroeconomic data is readily available, detailed, transaction-level information, or comprehensive sets of internal company documents, are considerably more difficult to obtain publicly. This report serves as a practical guide for AI developers and researchers, aiming to identify and detail publicly available, Nigerian-specific datasets across critical categories. It will provide direct access points (URLs and document names) where feasible, analyze the utility and limitations of each data source, and propose strategies for addressing persistent data gaps to foster robust AI development in this vital sector.

2. Financial Transaction Data: Availability and Alternatives
For the development of robust AI models in financial analysis and auditing, the ideal data would encompass raw ledger entries, trial balances, general ledgers, sub-ledgers (such as accounts payable, accounts receivable, inventory, and fixed assets), journal entries, and detailed bank statements. This level of granularity is crucial for automating financial data analysis, enabling precise account classification, performing substantive testing procedures, and generating comprehensive working papers.

Currently, direct access to raw, granular financial transaction data for individual entities or large-scale anonymized datasets is extremely limited in the public domain. This limitation is primarily due to stringent privacy regulations and the proprietary nature of such sensitive financial information. Financial institutions and corporations typically do not make this data publicly available. This presents a fundamental "granularity gap" where the detailed data needed for deep AI analysis is not publicly accessible. This situation necessitates a strategic approach for AI developers. For immediate AI applications, the focus must shift towards models that can effectively leverage aggregated data, such as those used for macroeconomic forecasting or high-level compliance checks. However, for AI applications demanding granular data, such as fraud detection or detailed audit analytics, generating synthetic data becomes a necessary approach, requiring specialized expertise in data synthesis and validation.

Despite these challenges, several alternatives and indirect sources can provide valuable information:

Aggregated Financial Data from Official Bodies
While not raw transaction data, aggregated financial data from central authorities can offer macro-level insights and trends that indirectly inform financial transaction analysis.

Central Bank of Nigeria (CBN): The CBN's "Data & Statistics" portal provides various financial data categories. This includes "Financial Data," "Money and Credit Statistics," "Money Market Indicators," "International Payments," "Statement of Assets & Liabilities," and "Flow of Funds Statistics". These are typically aggregated figures, offering a broad overview rather than individual transactions. This data is useful for understanding broader financial system liquidity, interest rate trends, and the impacts of monetary policy, which can provide a crucial context for micro-level transaction analysis. However, it is not suitable for direct ledger-level AI tasks. The data can be accessed at:    

https://www.cbn.gov.ng/rates/. 1    
Data & Statistics | Central Bank of Nigeria

cbn.gov.ng/rates

National Bureau of Statistics (NBS): The NBS provides aggregated economic data that can indirectly reflect financial activity. Relevant datasets include "Capital Importation" (quarterly data detailing inflows by type, sector, origin, and receiving bank), "Company Income Tax (CIT)" (quarterly data on aggregate CIT by sector), "Federation Account Allocation Committee (FAAC) Disbursement," "Foreign Trade in Goods Statistics," and "Gross Domestic Product (Production, Income and Expenditure Approach)". Many of these are listed as "Public use data files" on the NBS National Data Archive (NADA) portal. This information is valuable for macroeconomic forecasting, understanding capital flows, and analyzing sector-specific tax contributions. It can serve as high-level input for models predicting financial health or market trends, but it is not granular enough for direct transaction processing. The NBS website is    

https://www.nigerianstat.gov.ng/ , and its NADA portal is    

https://microdata.nigerianstat.gov.ng/index.php/catalog.   

The availability of high-quality, reliable, time-series data from central banks and statistical bureaus, driven by their mandates to monitor national economic health, means that AI models should be designed to incorporate multi-modal data. For example, a fraud detection model trained on synthetic transaction data could be enhanced by integrating macroeconomic indicators to identify patterns that correlate with broader economic shifts or industry-specific stress. This hybrid approach allows AI to not only detect micro-level anomalies but also understand their macro-economic context, thereby improving the robustness and interpretability of AI outputs.

Synthetic Data Generation
Given the pervasive privacy constraints, generating synthetic financial transaction data emerges as a crucial alternative for AI model training. Synthetic data is artificially generated information that mimics the statistical properties and patterns of real-world data without containing any actual sensitive details. This data can be fully synthetic, generated entirely through algorithms, or partially/hybrid, mixing real data with synthetic elements.   

A notable example is a "Synthetic Mobile Money Transaction Dataset" available on Kaggle, which is designed for fraud detection. This dataset is derived from real financial logs of an African mobile money service and includes transaction types (CASH-IN, CASH-OUT, DEBIT, PAYMENT, TRANSFER), amounts, and fraud labels. While not explicitly Nigerian, it demonstrates the feasibility and structure of such datasets for training. Furthermore, research has explored applying data mining techniques for financial fraud detection in Nigerian banks using individual bank statements and statutory bank charges. This research implies the use or generation of such data for study purposes, underscoring the potential of synthetic data in this domain. Synthetic data is highly valuable for training AI models for fraud detection, anomaly detection, automated classification, and substantive testing where real granular data is unavailable. It enables the testing of algorithms in varied scenarios, including rare events like fraud.   

Open Banking Nigeria Initiative
A forward-looking development in Nigeria is the Open Banking Nigeria initiative, which promises to enable consented, secure access to financial data through open APIs. The initiative is built on four core pillars: Privacy, Regulation (governed by CBN's framework), Guidelines, and API standards.   

This framework facilitates various use cases that leverage shared financial data to benefit businesses and individuals. These include business finance management (allowing SMEs to integrate bank accounts with accounting software for automation and cash flow management), personal finance management (aggregating financial data for spending insights and budgeting), enhanced credit scoring and lending, boosting financial inclusion by enabling account opening for unbanked Nigerians, and streamlined payment initiation (direct B2B transfers, online payments, automated recurring payments). This initiative, once fully mature and widely adopted, could provide the most direct and granular financial transaction data for AI applications in Nigeria, subject to user consent. AI developers should actively monitor its progress and engage with the framework as it evolves.   

Table 2.1: Overview of Financial Transaction Data Sources (Publicly Available & Alternatives)

Data Type	Source/Platform	Granularity	Access URL/Reference	Notes on Utility for AI
Aggregated Monetary Statistics	Central Bank of Nigeria (CBN)	Macro-level (Daily, Monthly, Quarterly, Annually)	
https://www.cbn.gov.ng/rates/    

Contextual analysis, understanding broader financial system liquidity and trends; not granular for individual transactions.
Capital Flows & Sectoral Aggregates	National Bureau of Statistics (NBS)	Quarterly/Sectoral Aggregates	
https://www.nigerianstat.gov.ng/, https://microdata.nigerianstat.gov.ng/index.php/catalog    

Macroeconomic forecasting, understanding capital importation trends, sectoral tax contributions; not for granular transaction processing.
Simulated Transaction Data	Kaggle (e.g., "Synthetic Mobile Money Transaction Dataset")	Simulated Transaction-level	
https://www.kaggle.com/datasets/sriharshaeedala/financial-fraud-detection-dataset    

Highly suitable for training AI models for fraud detection, anomaly detection, automated classification, and substantive testing where real data is unavailable.
Open Banking Framework	Open Banking Nigeria	API-driven (future potential for granular, consented data)	
https://openbanking.ng/    

Most promising future source for direct, granular financial transaction data, enabling advanced AI applications subject to user consent.
3. Financial Statement Data: Public Sources and Granularity
For AI applications focused on financial reporting, the required data includes annual and quarterly financial statements (Income Statement, Balance Sheet, Cash Flow Statement, Statement of Changes in Equity), along with their accompanying notes. This data is essential for automated compliance checks against financial reporting standards, performing ratio analysis for performance assessment, and assisting in the drafting of audit reports.

Key Public Sources
Nigerian Exchange Group (NGX): The NGX website is a primary source for financial statements of listed companies. The "Financial Information" section provides annual reports and quarterly financial statements for the NGX Group Plc itself, such as "NGX Annual Report 2024" and "NGX Group Q1 2025". More importantly, the "Corporate Disclosures" and "Company Results" sections are intended to host the financial statements of the 151 listed companies. While direct download links for all listed companies are not explicitly provided in the available information, these sections on the live site are the authoritative source for such data, likely accessible via a search function or dedicated company pages. The NGX also provides sector indices like the NGX Consumer Goods Index and NGX Banking Index , which can offer insights into specific industry performance. This data is highly valuable for training AI on financial statement analysis, ratio computation, trend analysis, and compliance checks (e.g., against IFRS as adopted in Nigeria). The NGX financial information can be found at:    

https://ngxgroup.com/financial-information/. A list of listed companies is available at:    

https://www.african-markets.com/en/stock-markets/ngse/listed-companies.   

National Bureau of Statistics (NBS): While the NBS does not provide individual company financial statements, it offers aggregated financial data that can serve as benchmarks or macro-level financial indicators. Datasets such as "Company Income Tax (CIT)" and "Capital Importation" provide aggregated financial performance metrics at a national or sectoral level. This information is useful for benchmarking, understanding industry-wide financial health, and contextualizing individual company performance within the broader economic landscape. The relevant data can be accessed via the NBS National Data Archive portal:    

https://microdata.nigerianstat.gov.ng/index.php/catalog/ECONS.   

Open Nigeria States: This platform provides audited financial statements for state governments. Examples include the "PLATEAU STATE AUDITED STATEMENT REPORT (FINANCIAL STATEMENT) DOCUMENT FOR THE YEAR 2022" and similar reports for other years and states. These documents are financial statement records that attest to the state's financial fairness. This data can be used for training AI on public sector financial reporting, budget analysis, and compliance with public finance regulations. It provides real-world examples of financial statements, albeit for governmental entities rather than private companies. Access these reports at:    

https://openstates.ng/plateau/data?search_term=Audited%20Statement  and    

https://openstates.ng/delta/dataset/1908/delta-state%20audited%20statement%20report%20(financial%20statement)%20document%20for%20the%20year%202023.   

The distinction between publicly available financial statements for listed companies and those for state governments highlights a "public vs. private" financial statement divide. AI models for financial statement analysis will need to be trained on diverse datasets depending on the target entity (corporate versus governmental). While the format of financial statements for companies might follow International Financial Reporting Standards (IFRS) as adopted in Nigeria, public sector accounting standards (IPSAS) would apply to government entities. This requires AI systems to be flexible enough to handle these variations, or specialized models may be needed for each domain to ensure accurate interpretation and analysis.   

Table 3.1: Public Sources for Nigerian Financial Statement Data

Data Type	Source/Platform	Granularity	Access URL/Reference	Notes on Utility for AI
Listed Company Financials	Nigerian Exchange Group (NGX)	Company-specific (Annual/Quarterly)	
https://ngxgroup.com/financial-information/ ,    

https://www.african-markets.com/en/stock-markets/ngse/listed-companies    

Primary source for public company financial analysis, ratio computation, trend analysis, and IFRS compliance checks.
Government Audited Statements	Open Nigeria States	State-level (Annual)	
https://openstates.ng/plateau/data?search_term=Audited%20Statement ,    

https://openstates.ng/delta/dataset/1908/delta-state%20audited%20statement%20report%20(financial%20statement)%20document%20for%20the%20year%202023    

Useful for public sector financial models, budget analysis, and compliance with public finance regulations.
Aggregated Sectoral Financials	National Bureau of Statistics (NBS)	Sectoral Aggregates (Quarterly)	
https://microdata.nigerianstat.gov.ng/index.php/catalog/ECONS    

Contextual benchmarking, understanding industry-wide financial health and performance trends.
4. Document Data: Sources for Document Intelligence
For AI applications in document intelligence, the ideal data would consist of scanned or digital copies of various financial and operational documents such as invoices, receipts, contracts, loan agreements, bank statements, payroll records, and human-readable internal policies. This data is vital for tasks like automated data extraction, validation, and comparing source documents to ledger entries during audit procedures.

Currently, direct public access to such sensitive, company-specific documents is virtually non-existent due to strict privacy regulations, the proprietary nature of internal business information, and security concerns. This presents a significant "document scarcity" challenge for AI development. AI applications requiring document intelligence, particularly for tasks like optical character recognition (OCR) and information extraction, must heavily rely on alternative strategies. Developers need to invest in robust synthetic data pipelines that can replicate the visual and textual complexities of real documents, including variations in scanning quality and layout. This also means that AI models trained on synthetic data will require rigorous validation with limited real-world samples (under non-disclosure agreements) to ensure real-world applicability.

Alternatives & Strategies
Synthetic Document Generation: Given the severe limitations in accessing real document data, synthetic generation is a critical necessity for training AI models for document intelligence. Synthetic data can effectively mimic real-world variability, including poorly scanned, crumpled, or faded documents. Research demonstrates the effectiveness of combining large language models (LLMs) with classic OCR for invoice scanning, showing improved accuracy and scalability in extracting information from diverse layouts. While specific Nigerian document datasets are not publicly detailed, the Consolidated Receipt Dataset (CORD) for post-OCR parsing, though Indonesian, illustrates the type of dataset needed, containing images and text annotations. This approach is crucial for training AI to extract fixed fields, semi-structured tables (like line items), and free-form notes from various document formats.   

Publicly Available Templates/Forms:

Corporate Affairs Commission (CAC): The CAC provides various official forms and templates relevant to corporate governance in Nigeria. Examples include "CAC 10 Annual Return for a Small Company," "CAC 2.4 Notice of Change of Authorised Share Capital," and "CAC/BN/7 Annual Returns for Business Name". While these are not filled documents, these templates can help AI understand the    

structure and types of information expected in official Nigerian corporate documents. The CAC forms can be accessed at: https://www.cac.gov.ng/forms/.   

Government Contract Portals (Limited Textual Data):

Nigeria Open Contracting Portal (NOCOPO): This portal tracks federal government contract files.   

Bureau of Public Procurement (BPP): The BPP website provides public procurement documents such as "Standard Bidding Documents" and "Request For Proposals".   


These sources offer some textual data related to contracts, but generally not the full contract text or granular financial details within them. They are more useful for understanding procurement processes and high-level contract awards rather than for detailed document intelligence tasks. The NOCOPO portal is at:    

https://nocopo.bpp.gov.ng/ , and BPP documents are at:    

https://www.bpp.gov.ng/all-downloads/.   

The availability of public sources like CAC providing document templates and forms highlights a "structural versus content" challenge. These resources offer valuable insights into the structure of Nigerian financial documents and the expected fields for information. However, they do not provide the    

content—the actual filled data. This means AI models can leverage these templates to learn expected layouts. However, to learn the actual data patterns and variability within those fields, synthetic data or limited access to real, anonymized content (e.g., via Open Banking or private partnerships) becomes indispensable. This suggests a hybrid approach where structural understanding derived from public templates is combined with content learning from synthetic or restricted real data.

5. Regulatory Data: Compliance and Reporting Standards
For AI applications focused on regulatory compliance and report drafting, the required data includes textual information from key Nigerian financial reporting standards (IFRS as adopted in Nigeria), the Companies and Allied Matters Act (CAMA 2020), Financial Reporting Council of Nigeria (FRCN) guidelines, International Standards on Auditing (ISAs), and Nigerian tax laws (such as Withholding Tax (WHT), Value Added Tax (VAT), and Companies Income Tax (CIT)). This data is fundamental for AI models to perform regulatory and compliance checks, and to assist in drafting various financial and audit reports.

Key Public Sources
Corporate Affairs Commission (CAC): The CAC provides the full text of the Companies and Allied Matters Act (CAMA) 2020. It also offers related regulations such as "Persons with Significant Control Regulations, 2022," "Insolvency Regulations 2022," and "Companies Regulations 2021". This legislative data is essential for AI models performing corporate governance compliance checks, legal entity analysis, and understanding the rules governing company formation and operation in Nigeria. The CAC resources are available at:    

https://www.cac.gov.ng/resources/.   

Financial Reporting Council of Nigeria (FRCN): The FRCN is the primary regulatory agency responsible for implementing the Financial Reporting Council of Nigeria Act 2011 (and its 2023 amendment), which mandates the adoption of IFRS and sets accounting and auditing standards in Nigeria. The FRCN has issued "Guidance on Management Report on Internal Control Over Financial Reporting (ICFR)" , which provides directives for Public Interest Entities (PIEs) to assess and report on the effectiveness of their internal controls. The FRC Act (as amended) 2023 also expands the definition of PIEs and outlines penalties for non-compliance. While direct access to the full text of adopted IFRS and ISAs on the FRCN website was not explicitly detailed in the provided information, it is stated that the FRC has the authority to adopt and keep up-to-date auditing standards and ensure consistency with international pronouncements, and that all standards are adopted as issued by the IAASB for application in Nigeria. This implies that IFRS and ISAs are effectively Nigerian standards. This textual data is critical for AI models performing financial reporting compliance, internal control evaluations, and adherence checks against auditing standards. Relevant information can be found at:    

https://ng.andersen.com/the-frc-issued-its-guidance-on-management-report-on-icfr/  and    

https://frcnigeria.gov.ng/wp-content/uploads/2024/09/FRC-FS-for-2022_compressed.pdf.   

Federal Inland Revenue Service (FIRS): The FIRS website is a comprehensive source for Nigerian tax laws, circulars, regulations, and public notices. Key tax legislation available includes the "Companies Income Tax Act (CITA)," "Value Added Tax Act (VAT)," "Personal Income Tax Act (PITA)," "Petroleum Profits Tax Act (PPTA)," "Capital Gains Tax Act (CGTA)," and "Stamp Duties Act (STD)". Additionally, the FIRS provides numerous tax circulars and public notices, such as "Guidelines on the implementation of Deduction of tax at Source (Withholding) Regulation, 2024," and "Tax Implications of the Adoption of the International Financial Reporting Standards (IFRS)". This extensive collection of tax-related documents is essential for AI models performing tax compliance, tax computation, and advisory services. The FIRS tax resources are available at:    

https://firs.gov.ng/tax-resources.   

Institute of Chartered Accountants of Nigeria (ICAN) & Association of National Accountants of Nigeria (ANAN): These professional bodies play a significant role in supporting the adoption and implementation of international accounting and auditing standards in Nigeria, including IFRS, ISAs, and the IESBA Code of Ethics. ICAN, for instance, regularly reviews its Quality Assurance (QA) system guidelines and offers Continuing Professional Development (CPD) courses on new standards like ISQM 1. ANAN also emphasizes continuous learning and ethical leadership within the profession. While not primary sources for the laws themselves, their websites offer resources, publications, and guidance on applying these standards in practice. This content can be valuable for training AI on the practical application of regulations and ethical considerations. ICAN's resources can be explored via their IFAC member page:    

https://www.ifac.org/about-ifac/membership/members/institute-chartered-accountants-nigeria , and ANAN's resources at:    

https://anan.org.ng/resources/.   

The Nigerian regulatory environment is characterized by frequent amendments and new guidelines, as evidenced by the amended FRC Act in 2023  and regular issuance of new tax regulations by FIRS. This dynamic nature implies that AI systems designed for compliance must incorporate mechanisms for continuous monitoring and rapid updating of their regulatory knowledge bases. A static AI model will quickly become obsolete. This necessitates robust data pipelines for ingesting new legal texts and potentially advanced natural language processing (NLP) capabilities to interpret and integrate changes into existing compliance rules.   

Furthermore, while the textual content of laws and standards is available, their practical application often involves nuanced interpretations, professional judgment, and industry-specific practices. Professional bodies like ICAN and ANAN provide guidance and training that reflect these practical interpretations. This means that AI models should not solely rely on raw legal text but also incorporate data that captures these interpretations. This could involve training AI on case studies, expert commentaries, and anonymized audit findings that illustrate how regulations are applied in real-world scenarios. Collaboration with professional bodies or access to their technical helpdesks could provide valuable qualitative data for fine-tuning AI's understanding of regulatory nuances.   

Table 5.1: Public Sources for Nigerian Regulatory Data

Data Type	Source/Platform	Content/Focus	Access URL/Reference	Notes on Utility for AI
Corporate Law & Regulations	Corporate Affairs Commission (CAC)	CAMA 2020, Persons with Significant Control, Insolvency, Companies Regulations	
https://www.cac.gov.ng/resources/    

Essential for corporate governance compliance, legal entity analysis, and company operational rules.
Financial Reporting & Audit Standards	Financial Reporting Council of Nigeria (FRCN)	IFRS adoption, ICFR guidance, Auditing Standards (IAASB adopted)	
https://ng.andersen.com/the-frc-issued-its-guidance-on-management-report-on-icfr/ ,    

https://frcnigeria.gov.ng/wp-content/uploads/2024/09/FRC-FS-for-2022_compressed.pdf    

Critical for financial reporting compliance, internal control evaluations, and audit standard adherence checks.
Tax Laws & Regulations	Federal Inland Revenue Service (FIRS)	CITA, VAT, PITA, PPTA, CGTA, Stamp Duties Act, Tax Circulars, Regulations, Public Notices	
https://firs.gov.ng/tax-resources    

Indispensable for tax compliance, computation, and advisory services.
Professional Guidance & Ethics	ICAN & ANAN	Interpretation of standards, CPD materials, Code of Ethics (IESBA adopted)	
https://www.ifac.org/about-ifac/membership/members/institute-chartered-accountants-nigeria ,    

https://anan.org.ng/resources/    

Valuable for understanding practical application of regulations and ethical considerations in professional practice.
6. Audit Working Papers/Reports: Challenges and Proxy Data
For AI applications in auditing, the ideal data would include anonymized historical audit working papers, lead schedules, audit reports, management letters, and internal audit reports. This data is valuable for training AI on tasks such as report drafting, working paper generation, and understanding common audit findings and their resolution.

However, direct public access to anonymized audit working papers and detailed internal audit reports is extremely rare. This is due to the inherent confidentiality of client information, client privilege, and the proprietary methodologies employed by audit firms. This presents a significant "confidentiality barrier" to data access. AI development for automating audit working paper generation or detailed audit finding analysis will depend almost entirely on synthetic data. This requires a deep understanding of auditing standards (International Standards on Auditing - ISAs) and practices to generate realistic data that reflects audit procedures, evidence gathering, and conclusion formulation. Partnerships with audit firms, under strict non-disclosure agreements for data synthesis, could be explored to ensure the realism and utility of such synthetic datasets.

Proxy Data & Alternatives
Government Audited Statements (Limited Scope):

Open Nigeria States: This platform provides "Audited Statement Reports (Financial Statement) Document" for various states and years, such as the "PLATEAU STATE AUDITED STATEMENT REPORT (FINANCIAL STATEMENT) DOCUMENT FOR THE YEAR 2022". It is important to note that these are the    

outputs of an audit, specifically the final financial statements and the auditor's opinion, rather than the detailed underlying working papers. This data can be used to train AI on the structure and content of final audit reports for public sector entities, and to identify the types of financial statements that are subject to audit. Access these reports at: https://openstates.ng/plateau/data?search_term=Audited%20Statement  and    

https://openstates.ng/delta/dataset/1908/delta-state%20audited%20statement%20report%20(financial%20statement)%20document%20for%20the%20year%202023.   

Internal Audit Reports (Conceptual Examples):

A UNICEF internal audit report for the Nigeria Country Office (2020/12) is publicly available. This document outlines audit objectives, scope, key risks (including fraud, corruption, and security), and agreed actions. It also mentions recurring concerns and the "fraud triangle" framework. This report provides a conceptual understanding of internal audit processes, risk identification, and reporting structure. It is a high-level report, not granular working papers, but offers valuable insights into the nature of audit findings and management responses in a real-world (though non-corporate) context. The report is available at:    

https://www.unicef.org/auditandinvestigation/media/1526/file/2020%20OIAI%20Audit%20Report%20Nigeria.pdf.   

Academic/Theoretical Resources on Audit Documentation:

Presentations available on platforms like SlideShare discuss audit working paper purposes, contents, organization (e.g., permanent and current files), and types of audit evidence. These are educational resources that can help AI understand the    

principles and structure of audit documentation, even in the absence of real-world examples. Such resources can be found at: https://www.slideshare.net/slideshow/audit-workingpapers/54853222.   

Synthetic Data Generation: Given the extreme scarcity of real-world audit documentation, synthetic generation of audit working papers, lead schedules, and management letters is likely the most viable path for training AI on these specific tasks. This would involve creating realistic but non-sensitive data that mimics the format, content, and interconnections found in actual audit documentation.

The publicly available "audit reports," such as those from Open Nigeria States, represent the final outputs of an audit, not the detailed process documentation (working papers) that leads to them. Similarly, the UNICEF report provides a high-level overview of an internal audit but lacks the granular steps or evidence. This highlights a "output versus process" data discrepancy. AI models aimed at    

generating working papers or performing substantive or compliance testing require data that illustrates the audit process and the evidence collected, not just the final conclusions. This further reinforces the need for synthetic data that can simulate the entire audit trail, from initial planning and risk assessment to detailed testing and documentation. Academic materials on audit documentation can provide the theoretical framework for this synthesis.   

7. Risk Data: Identification and Control Evaluation
For AI applications in risk identification and control evaluation, the ideal data would be labeled with identified risks, internal control weaknesses, fraud indicators, and related party transactions. This information is crucial for training AI to proactively identify potential issues and assess the effectiveness of internal controls.

However, data related to risk and internal control is highly sensitive and proprietary, making direct public access extremely limited. This includes specific control weaknesses, detailed fraud indicators, or sensitive related party transactions. This "sensitive nature of risk data" means that AI models for risk identification and control evaluation will primarily rely on two approaches: synthetic data and regulatory frameworks as knowledge bases. For training on specific fraud patterns, control deficiencies, or related party transaction indicators, synthetic data generation with carefully labeled risk scenarios is indispensable. Alternatively, AI can be trained on regulatory texts, such as the FRCN's ICFR guidance, to understand what constitutes a control and how it should be evaluated, even without real-world examples of control failures. This allows AI to assess compliance against established standards.

Proxy Data & Alternatives
Fraud Research Datasets (Synthetic/Conceptual):

A Kaggle dataset describes a "Synthetic Mobile Money Transaction Dataset" that includes "isFraud" labels, designed for fraud detection research. While synthetic and not explicitly Nigerian, it demonstrates the structure of data suitable for training AI to identify fraud.   

Research on financial fraud detection in Nigerian banks has utilized data mining techniques on "individual bank statements and statutory bank charges" to identify fraudulent transactions. This implies the use or generation of data with embedded fraud indicators.   

A news report highlights the rise of "synthetic identity fraud" in Nigeria's financial sector, noting a significant increase in synthetic document fraud. This underscores the growing relevance of synthetic data for understanding and combating evolving fraud schemes. These datasets, particularly synthetic ones, are vital for training AI models to identify fraud patterns and anomalies.   

Relevant URLs: https://www.kaggle.com/datasets/sriharshaeedala/financial-fraud-detection-dataset ,    

https://iiardjournals.org/get/IJCSMT/VOL.%2010%20NO.%203%202024/Financial%20fraud%20detection%2045-66.pdf ,    

https://www.vanguardngr.com/2025/06/identity-theft-nigeria-faces-rising-synthetic-id-threats-despite-fall-in-traditional-fraud-methods/.   

Regulatory Guidance on Internal Controls:

Financial Reporting Council of Nigeria (FRCN): The FRCN has issued "Guidance on Management Report on Internal Control Over Financial Reporting (ICFR)". This guidance provides directives for Public Interest Entities (PIEs) on how to assess and report on the effectiveness of their internal controls over financial reporting, emphasizing adequate documentation and annual assessment. This textual data is crucial for training AI to understand the    

framework and requirements for internal control evaluation, even in the absence of raw control testing data. This document is available at: https://ng.andersen.com/the-frc-issued-its-guidance-on-management-report-on-icfr/.   

Internal Audit Reports (High-Level Risk Identification):

The UNICEF Nigeria Country Office internal audit report discusses operational risks, including fraud, corruption, and security, and references the "fraud triangle". This report offers examples of high-level risk identification and control weaknesses from a real-world context, albeit for a non-corporate entity. It can inform AI models about the types of risks encountered and the general approach to reporting them. The report can be accessed at:    

https://www.unicef.org/auditandinvestigation/media/1526/file/2020%20OIAI%20Audit%20Report%20Nigeria.pdf.   

Open Banking Nigeria (Future Potential): While primarily designed for facilitating financial transactions, the Open Banking framework's ability to aggregate financial data for purposes like credit scoring and lending implies a future potential for identifying risk factors. This could include detecting unusual spending patterns or assessing debt levels in real-time. This offers a promising avenue for real-time risk monitoring based on consented financial data.   

A key aspect of risk data is the "proactive versus reactive" data challenge. Much of the publicly available "risk" data, such as fraud research datasets, is often designed for reactive fraud detection—identifying fraud after it has already occurred. However, the requirement for "risk data labeled with identified risks, internal control weaknesses" suggests a need for data that supports    

proactive risk identification and control evaluation. AI models for proactive risk management require datasets that capture not just instances of fraud, but also the precursors to fraud, control design deficiencies, and operational weaknesses. This type of data is even more sensitive and consequently harder to obtain. Therefore, AI development in this area will heavily rely on expert-defined rules, the simulation of various risk scenarios, and potentially a blend of synthetic data that explicitly models control environments and their vulnerabilities. The FRCN guidance on ICFR provides a conceptual foundation for building such scenarios.   

8. Economic & Industry Data: Forecasting and Advisory
For AI applications in financial forecasting and advisory services, the required data includes a wide range of macroeconomic indicators, industry-specific financial benchmarks, and market trends. This comprehensive data set is crucial for developing models that can predict economic shifts, assess industry performance, and provide strategic recommendations.

Key Public Sources
Central Bank of Nigeria (CBN): The CBN's "Data & Statistics" portal is a rich source of macroeconomic information. It offers "Economic/Macro Indicators," "Exchange Rates," "Inflation," "Gross Domestic Product - Nominal," "Gross Domestic Product - Real," "Crude Oil Price," and "Money Market Indicators". Additionally, the CBN provides "Statistical Bulletins (Annual/Quarterly)," the "Purchasing Managers' Index," and "Statistical Expectations Survey Reports" covering business, consumer, credit conditions, and inflation attitudes/expectations. This data is comprehensive for macroeconomic forecasting, monetary policy analysis, and understanding financial market dynamics. The CBN data is available at:    

https://www.cbn.gov.ng/rates/.   

National Bureau of Statistics (NBS): The NBS is a fundamental source for detailed economic and industry data. It provides detailed GDP reports (including oil/non-oil sectors and sector-specific growth rates), Capital Importation data, Consumer Price Index (CPI) and inflation rates (All-Items, Core, Food), and commodity prices (Premium Motor Spirit (PMS), Automotive Gas Oil (AGO), National Household Kerosene (NHK), and Liquefied Petroleum Gas (LPG)). The NBS also operates an "Open Data Portal (ODP)" and a "National Data Archive (NADA)" that host various datasets, including "Consumer Price Index and Inflation," "Nigeria Labour Force Survey," "Capital Importation," "Company Income Tax," and "Foreign Trade in Goods Statistics". This information is essential for detailed economic analysis, industry performance benchmarking, and forecasting key economic variables. The NBS main website is    

https://www.nigerianstat.gov.ng/ , its Code for Africa portal is    

https://nigerianstat.dev.codeforafrica.org/ , the Open Data Portal is    

https://nigeria.opendataforafrica.org/ , and the NADA portal is    

https://microdata.nigerianstat.gov.ng/index.php/catalog.   

Kaggle Datasets (User-Contributed Economic Data): Kaggle hosts several user-contributed datasets that aggregate Nigerian economic data, often in a readily usable format. Examples include:

"Nigeria Inflation Rates" (March 2003-June 2024), which provides monthly inflation rates, crude oil prices, production/export levels, and various CPI components.   

"Nigerian Financial Markets Data" (2006-2025), containing monthly money market indicators such as Inter-Bank Call Rate, Monetary Policy Rate (MPR), and Treasury Bill Rate.   

"Nigeria Economy Growth 1990-2023," which includes time series data on GDP, inflation, unemployment, government debt, and sectoral contributions (agriculture, industry, services).   


These datasets offer readily available, often pre-cleaned data suitable for time series analysis, forecasting, and economic modeling.

Relevant URLs: https://www.kaggle.com/datasets/iamhardy/nigeria-inflation-rates/data ,    

https://www.kaggle.com/datasets/sodipepaul/nigerian ,    

https://github.com/Jamaderibigbe/Nigeria-Economy-Growth-1990-2023--Excel ,    

https://github.com/OOA-py/Nigeria-Economy-Analysis-and-Forecasting.   

World Bank: The World Bank's Nigeria country page provides various economic indicators, including GDP (current US$, per capita, and annual growth), unemployment rates, consumer price inflation, and personal remittances as a percentage of GDP. It also offers a "Financial Sector Indicators for Nigeria" dataset, which includes detailed metrics on the banking sector, financial inclusion, monetary indicators, capital markets, and remittances. This global perspective, coupled with long time series and detailed financial sector metrics, is invaluable for economic modeling and comparative analysis. The World Bank data for Nigeria can be found at:    

https://data.worldbank.org/country/nigeria  and    

https://data.humdata.org/dataset/world-bank-financial-sector-indicators-for-nigeria.   

International Monetary Fund (IMF): The IMF's Nigeria page offers "At a Glance" economic indicators, including projected real GDP change, projected consumer prices, and population data. It also provides access to Article IV Staff Reports and various publications that offer high-level economic assessments, policy recommendations, and projections for Nigeria's economy. This information is particularly valuable for strategic advisory services. The IMF's Nigeria page is at:    

https://www.imf.org/en/Countries/NGA.   

African Development Bank (AfDB): The AfDB's Nigeria country page provides an "Nigeria Economic Outlook" section with data on GDP growth, inflation, exchange rates, fiscal deficit, public debt, and current account surplus. It also offers "Country Diagnostic Note" and "Country Strategy Paper" documents that detail Nigeria's development constraints and intervention strategies. This source offers a regional perspective, detailed economic analysis, and insights into development challenges and opportunities. The AfDB's Nigeria page is at:    

https://www.afdb.org/en/countries/west-africa/nigeria , and specific documents like the "Nigeria Country Diagnostic Note 2023" are available at:    

https://www.afdb.org/sites/default/files/documents/projects-and-operations/nigeria_country_diagnostic_note_2023.pdf.   

While macroeconomic data is abundant, its aggregate nature means it is best suited for high-level economic forecasting and strategic advisory, rather than granular, entity-specific financial predictions. This implies that AI models for economic forecasting should leverage the extensive time-series data from CBN, NBS, World Bank, and IMF to predict national or sectoral trends. However, for precise, company-level financial forecasting, these macro indicators serve as contextual overlays rather than direct input for granular revenue or expense prediction. The challenge lies in downscaling macro trends to micro-level impacts, which often requires additional proprietary or synthetic data.

The various national and international bodies providing economic data offer a unique perspective and level of detail. For example, CBN focuses on monetary policy, NBS on national statistics, the World Bank on development indicators, and the IMF on macroeconomic stability. A holistic AI approach for economic and industry analysis should integrate data from multiple sources to gain a comprehensive understanding. This multi-source integration can enhance the robustness of forecasts and advisory services by cross-validating information and capturing a broader range of economic influences. For example, combining NBS's detailed CPI data with CBN's interest rates and IMF's policy recommendations can lead to more nuanced inflation forecasting models.   

Table 8.1: Public Sources for Nigerian Economic & Industry Data

Data Type	Source/Platform	Granularity	Access URL/Reference	Notes on Utility for AI
Macroeconomic Indicators & Monetary Policy	Central Bank of Nigeria (CBN)	Daily, Monthly, Quarterly, Annually	
https://www.cbn.gov.ng/rates/    

Comprehensive for macroeconomic forecasting, monetary policy analysis, and financial market dynamics.
National Statistics & Sectoral Performance	National Bureau of Statistics (NBS)	Quarterly, Monthly, Annual	
https://www.nigerianstat.gov.ng/ ,    

https://nigeria.opendataforafrica.org/ ,    

https://microdata.nigerianstat.gov.ng/index.php/catalog    

Essential for detailed economic analysis, industry benchmarking, and forecasting key economic variables.
Curated Economic Datasets	Kaggle, GitHub	Monthly, Annual time series	
https://www.kaggle.com/datasets/iamhardy/nigeria-inflation-rates/data ,    

https://www.kaggle.com/datasets/sodipepaul/nigerian ,    

https://github.com/Jamaderibigbe/Nigeria-Economy-Growth-1990-2023--Excel    

Readily available, often pre-cleaned datasets for time series analysis, forecasting, and economic modeling.
Global Economic & Financial Sector Indicators	World Bank	Annual, Various Frequencies	
https://data.worldbank.org/country/nigeria ,    

https://data.humdata.org/dataset/world-bank-financial-sector-indicators-for-nigeria    

Global perspective, long time series, and detailed financial sector metrics for economic modeling and comparative analysis.
Macroeconomic Assessments & Policy Projections	International Monetary Fund (IMF)	Annual, Projections	
https://www.imf.org/en/Countries/NGA    

High-level economic assessments, policy recommendations, and projections valuable for strategic advisory.
Regional Economic Outlook & Development Strategy	African Development Bank (AfDB)	Annual, Various Frequencies	
https://www.afdb.org/en/countries/west-africa/nigeria ,    

https://www.afdb.org/sites/default/files/documents/projects-and-operations/nigeria_country_diagnostic_note_2023.pdf    

Regional perspective, detailed economic analysis, and insights into development challenges and opportunities.
9. Conclusions and Recommendations
The landscape of publicly available, Nigerian-specific datasets for AI-driven financial and audit automation presents a mixed picture. While there is a robust foundation of macroeconomic indicators and comprehensive regulatory texts, significant gaps persist in the availability of granular financial transaction data, detailed internal company documents, and anonymized audit working papers. These limitations are primarily driven by data privacy concerns, the proprietary nature of financial information, and the evolving stage of data infrastructure and sharing initiatives in Nigeria.

The analysis indicates that AI developers must adopt a multi-faceted strategy to overcome these data challenges.

Key Recommendations:

Prioritize Official Government Portals for Aggregated Data and Regulatory Texts: Official sources like the Central Bank of Nigeria (CBN), National Bureau of Statistics (NBS), Federal Inland Revenue Service (FIRS), and Corporate Affairs Commission (CAC) provide reliable and authoritative macroeconomic data, financial aggregates, and comprehensive regulatory frameworks. These are indispensable for AI models requiring contextual understanding, high-level compliance checks, and adherence to legal and reporting standards.

Strategically Employ Synthetic Data Generation: For AI models that require granular financial transactions, detailed internal documents (such as invoices and contracts), and audit working papers, where real data is largely inaccessible, synthetic data generation is not merely an option but a critical necessity. This approach demands a deep understanding of the underlying financial processes and auditing standards to ensure the generated data is realistic and representative. Investment in robust synthetic data pipelines and validation methodologies is paramount.

Actively Monitor and Engage with Open Banking Nigeria: The Open Banking Nigeria initiative represents the most promising future source of consented, granular financial data. As this framework matures and gains wider adoption, it holds the potential to unlock direct access to transactional information, which would significantly enhance the capabilities of AI applications in financial management, credit scoring, and payment processing. AI developers should actively monitor its progress and prepare to integrate with its API standards.

Adopt Multi-Modal Data Integration: To maximize the effectiveness of AI models, it is advisable to combine macro-economic indicators from official sources with synthetic micro-data. This multi-modal approach provides AI models with both a broad contextual understanding of the Nigerian economy and the granular detail necessary for specific financial and audit tasks. Such integration can lead to more robust forecasts, more accurate anomaly detection, and more nuanced advisory services.

Implement Continuous Regulatory Monitoring: Given the dynamic nature of Nigerian regulatory frameworks, AI systems designed for compliance must incorporate mechanisms for continuous monitoring and rapid updating of their knowledge bases. This ensures that AI-driven compliance checks and report drafting remain aligned with the latest legal and reporting standards, preventing obsolescence and maintaining accuracy.

Explore Collaborative Partnerships for Data Realism: To enhance the realism and utility of synthetic datasets and to validate AI models, exploring partnerships with financial institutions and audit firms is highly recommended. While direct data sharing may be limited, collaborations under strict confidentiality agreements could provide essential insights into real-world data characteristics, operational nuances, and audit practices, thereby improving the fidelity of synthetic data and the practical applicability of AI solutions.

