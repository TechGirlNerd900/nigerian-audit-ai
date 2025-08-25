import logging
import os
import json
import pandas as pd
from typing import Dict, List, Any
import asyncio
from ..scrapers.ngx_scraper import NGXScraper
from ..scrapers.frc_scraper import FRCScraper
from ..utils.document_parser import DocumentParser

logger = logging.getLogger(__name__)

class TrainingDataCollector:
    """Collect and prepare training data for Nigerian audit AI models"""
    
    def __init__(self):
        self.data_dir = "data"
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        self.training_dir = os.path.join(self.data_dir, "training")
        self.regulations_dir = os.path.join(self.data_dir, "regulations")
        
        # Create directories
        for dir_path in [self.raw_dir, self.processed_dir, self.training_dir, self.regulations_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    async def collect_all_data(self):
        """Collect all training data from various sources"""
        
        logger.info("Starting comprehensive training data collection...")
        
        # Collect from scrapers
        await self._collect_from_scrapers()

        # Collect regulatory documents
        await self.collect_regulatory_documents()
        
        # Collect custom PDF data
        self.collect_custom_pdf_data()
        
        # Collect synthetic data
        self._generate_synthetic_data()
        
        # Process and prepare training datasets
        self.prepare_training_datasets()
        
        logger.info("Training data collection completed")
    
    async def _collect_from_scrapers(self):
        """Collect data from web scrapers"""
        
        logger.info("Collecting data from Nigerian financial sources...")
        
        # NGX data
        ngx_scraper = NGXScraper()
        async with ngx_scraper:
            ngx_data = await ngx_scraper.collect_data()
        
        # FRC data
        frc_scraper = FRCScraper()
        async with frc_scraper:
            frc_data = await frc_scraper.collect_data()
        
        logger.info("Web scraping completed")

    async def collect_regulatory_documents(self):
        """Collect and process regulatory documents from FRC"""
        logger.info("Collecting and processing regulatory documents...")
        frc_scraper = FRCScraper()
        async with frc_scraper:
            documents = await frc_scraper.collect_data()

        parser = DocumentParser()
        processed_docs = []
        for doc in documents:
            if doc['type'] == 'pdf':
                text = parser.parse_pdf(doc['content'])
            else:
                text = parser.parse_html(doc['content'])
            
            processed_docs.append({
                'source': doc['source'],
                'title': doc['title'],
                'text': text
            })
        self._save_data(processed_docs, "processed_regulations.json", directory=self.regulations_dir)

    def _generate_synthetic_data(self):
        """Generate synthetic training data for models"""
        
        logger.info("Generating synthetic training data...")
        
        # Generate financial statements training data
        financial_training_data = self._generate_financial_training_data()
        self._save_data(financial_training_data, "financial_training_data.json")
        
        # Generate compliance training data
        compliance_training_data = self._generate_compliance_training_data()
        self._save_data(compliance_training_data, "compliance_training_data.json")
        
        # Generate risk assessment training data
        risk_training_data = self._generate_risk_training_data()
        self._save_data(risk_training_data, "risk_training_data.json")

        trial_balance_training_data = self._generate_trial_balance_training_data()
        self._save_data(trial_balance_training_data, "trial_balance_training_data.json")

        document_intelligence_training_data = self._generate_document_intelligence_training_data()
        self._save_data(document_intelligence_training_data, "document_intelligence_training_data.json")
        
        logger.info("Synthetic data generation completed")
    
    def _generate_financial_training_data(self) -> List[Dict]:
        """Generate financial analysis training examples"""
        
        import random
        
        training_examples = []
        
        # Generate 1000 training examples
        for i in range(1000):
            
            # Generate random financial data
            revenue = random.uniform(10_000_000, 1_000_000_000)  # ₦10M to ₦1B
            current_assets = random.uniform(revenue * 0.2, revenue * 0.8)
            current_liabilities = random.uniform(current_assets * 0.3, current_assets * 0.9)
            total_assets = random.uniform(current_assets * 1.2, current_assets * 3.0)
            total_liabilities = random.uniform(total_assets * 0.3, total_assets * 0.8)
            net_income = random.uniform(revenue * -0.1, revenue * 0.2)
            
            # Calculate ratios
            current_ratio = current_assets / current_liabilities
            debt_to_equity = total_liabilities / (total_assets - total_liabilities)
            profit_margin = net_income / revenue
            roa = net_income / total_assets
            
            # Determine risk level based on ratios
            risk_score = 100
            
            if current_ratio < 1.0:
                risk_score -= 30
            elif current_ratio > 3.0:
                risk_score -= 10
            
            if debt_to_equity > 1.0:
                risk_score -= 25
            
            if profit_margin < 0:
                risk_score -= 40
            elif profit_margin < 0.05:
                risk_score -= 20
            
            if roa < 0:
                risk_score -= 20
            
            # Classify risk level
            if risk_score >= 80:
                risk_level = 0  # Low
            elif risk_score >= 60:
                risk_level = 1  # Medium
            elif risk_score >= 40:
                risk_level = 2  # High
            else:
                risk_level = 3  # Critical
            
            example = {
                'id': f'financial_{i+1}',
                'financial_data': {
                    'revenue': revenue,
                    'current_assets': current_assets,
                    'current_liabilities': current_liabilities,
                    'total_assets': total_assets,
                    'total_liabilities': total_liabilities,
                    'net_income': net_income
                },
                'ratios': {
                    'current_ratio': current_ratio,
                    'debt_to_equity': debt_to_equity,
                    'profit_margin': profit_margin,
                    'return_on_assets': roa
                },
                'risk_level': risk_level,
                'risk_score': risk_score,
                'industry': random.choice(['manufacturing', 'banking', 'oil_gas', 'telecommunications', 'retail']),
                'company_size': random.choice(['small', 'medium', 'large'])
            }
            
            training_examples.append(example)
        
        return training_examples
    
    def _generate_compliance_training_data(self) -> List[Dict]:
        """Generate compliance training examples"""
        
        import random
        
        training_examples = []
        
        # Generate 500 compliance examples
        for i in range(500):
            
            # Random company data
            annual_revenue = random.uniform(5_000_000, 2_000_000_000)
            is_public = random.choice([True, False])
            employee_count = random.randint(10, 5000)
            
            # Determine company size
            if annual_revenue <= 25_000_000:
                company_size = 0  # Small
            elif annual_revenue <= 500_000_000:
                company_size = 1  # Medium
            else:
                company_size = 2  # Large
            
            # Generate compliance violations
            violations = []
            
            # FRC violations
            if is_public or annual_revenue > 500_000_000:
                if random.random() < 0.3:  # 30% chance of FRC violation
                    violations.append('FRC')
            
            # FIRS violations
            if random.random() < 0.2:  # 20% chance of FIRS violation
                violations.append('FIRS')
            
            # CAMA violations
            if random.random() < 0.15:  # 15% chance of CAMA violation
                violations.append('CAMA')
            
            # CBN violations (only for banks)
            industry = random.choice(['manufacturing', 'banking', 'oil_gas', 'telecommunications', 'retail'])
            if industry == 'banking' and random.random() < 0.25:
                violations.append('CBN')
            
            example = {
                'id': f'compliance_{i+1}',
                'company_size': company_size,
                'industry_type': {'manufacturing': 0, 'banking': 1, 'oil_gas': 2, 'telecommunications': 3, 'retail': 4}[industry],
                'is_public': 1 if is_public else 0,
                'annual_revenue': annual_revenue,
                'total_assets': annual_revenue * random.uniform(1.2, 3.0),
                'employee_count': employee_count,
                'violations': violations
            }
            
            training_examples.append(example)
        
        return training_examples
    
    def _generate_risk_training_data(self) -> List[Dict]:
        """Generate risk assessment training examples"""
        
        import random
        
        training_examples = []
        
        # Generate 800 risk assessment examples
        for i in range(800):
            
            # Generate risk factors
            liquidity_risk = random.uniform(0, 100)
            credit_risk = random.uniform(0, 100)
            operational_risk = random.uniform(0, 100)
            market_risk = random.uniform(0, 100)
            regulatory_risk = random.uniform(0, 100)
            
            # Calculate overall risk score
            overall_risk = (
                liquidity_risk * 0.25 +
                credit_risk * 0.20 +
                operational_risk * 0.25 +
                market_risk * 0.20 +
                regulatory_risk * 0.10
            )
            
            # Determine risk level
            if overall_risk >= 80:
                risk_level = 0  # Low
            elif overall_risk >= 60:
                risk_level = 1  # Medium
            elif overall_risk >= 40:
                risk_level = 2  # High
            else:
                risk_level = 3  # Critical
            
            example = {
                'id': f'risk_{i+1}',
                'liquidity_risk': liquidity_risk,
                'credit_risk': credit_risk,
                'operational_risk': operational_risk,
                'market_risk': market_risk,
                'regulatory_risk': regulatory_risk,
                'overall_risk_score': overall_risk,
                'risk_level': risk_level,
                'industry': random.choice(['manufacturing', 'banking', 'oil_gas', 'telecommunications', 'retail']),
                'company_size': random.choice([0, 1, 2])  # small, medium, large
            }
            
            training_examples.append(example)
        
        return training_examples

    def _generate_trial_balance_training_data(self) -> List[Dict]:
        """Generate a more complex synthetic trial balance."""
        
        import random
        
        training_examples = []
        total_debits = 0
        total_credits = 0
        
        # Define account classifications with more details
        account_classifications = {
            'Cash and Cash Equivalents': [('1010', 'Cash on Hand'), ('1020', 'First Bank'), ('1030', 'Zenith Bank'), ('1040', 'Petty Cash Float')],
            'Receivables': [('1110', 'Trade Debtors - Local'), ('1120', 'Accounts Receivable - Export'), ('1130', 'Staff Loans and Advances')],
            'Inventory': [('1210', 'Raw Materials - Cement'), ('1220', 'Work in Progress - Construction'), ('1230', 'Finished Goods - Packaged Foods')],
            'Property, Plant, and Equipment': [('1310', 'Land and Buildings'), ('1320', 'Plant & Machinery'), ('1330', 'Motor Vehicles at Cost'), ('1340', 'Furniture & Fittings')],
            'Intangible Assets': [('1410', 'Goodwill on Acquisition'), ('1420', 'Software Licenses')],
            'Payables': [('2010', 'Trade Creditors - Local'), ('2020', 'Accrued Expenses - Salaries'), ('2030', 'Other Payables')],
            'Long-term Debt': [('2110', 'Bank of Industry Loan'), ('2120', '5-Year Corporate Bond')],
            'Equity': [('3010', 'Ordinary Share Capital'), ('3020', 'Retained Earnings b/f'), ('3030', 'Share Premium Account')],
            'Revenue': [('4010', 'Sales - Lagos'), ('4020', 'Sales - Abuja'), ('4030', 'Service Income')],
            'Cost of Sales': [('5010', 'Cost of Goods Sold'), ('5020', 'Direct Labour - Factory'), ('5030', 'Factory Overhead Allocation')],
            'Operating Expenses': [('6010', 'Salaries and Wages - Admin'), ('6020', 'Rent Expense - Office'), ('6030', 'Generator Fuel and Maintenance'), ('6040', 'Depreciation Expense'), ('6050', 'Amortization of Intangibles')],
            'Finance Costs': [('7010', 'Interest on Bank Loan'), ('7020', 'Bank Transaction Charges')],
            'Taxation': [('8010', 'Company Income Tax Provision'), ('8020', 'VAT Payable'), ('8030', 'WHT Payable')]
        }
        
        # Generate examples
        for classification, accounts in account_classifications.items():
            for account_code, account_name in accounts:
                debit = 0
                credit = 0
                
                if classification in ['Cash and Cash Equivalents', 'Receivables', 'Inventory', 'Property, Plant, and Equipment', 'Intangible Assets', 'Cost of Sales', 'Operating Expenses', 'Finance Costs']:
                    debit = round(random.uniform(100000, 50000000), 2)
                    total_debits += debit
                else:
                    credit = round(random.uniform(100000, 50000000), 2)
                    total_credits += credit
                    
                training_examples.append({
                    'account_code': account_code,
                    'account_name': account_name,
                    'debit': debit,
                    'credit': credit,
                    'classification': classification
                })
                
        # Balance the trial balance
        imbalance = round(total_debits - total_credits, 2)
        if imbalance > 0:
            # Add to a credit account (e.g., retained earnings)
            for example in training_examples:
                if example['account_code'] == '3020':
                    example['credit'] += imbalance
                    total_credits += imbalance
                    break
        else:
            # Add to a debit account (e.g., cash)
            for example in training_examples:
                if example['account_code'] == '1020':
                    example['debit'] += abs(imbalance)
                    total_debits += abs(imbalance)
                    break
                    
        return training_examples

    def _generate_document_intelligence_training_data(self) -> List[Dict]:
        """Generate training data for document intelligence model."""
        
        training_examples = []
        
        # Generate synthetic invoices
        for i in range(100):
            training_examples.append({
                'text': f'Invoice No: INV{i+1}\nDate: 01/01/2023\nTotal Amount: {1000.00 + i*100}',
                'document_type': 'invoice',
                'entities': {
                    'invoice_number': f'INV{i+1}',
                    'date': '01/01/2023',
                    'total_amount': 1000.00 + i*100
                }
            })
            
        # Generate synthetic receipts
        for i in range(100):
            training_examples.append({
                'text': f'Receipt No: REC{i+1}\nDate: 01/01/2023\nTotal Amount: {500.00 + i*50}',
                'document_type': 'receipt',
                'entities': {
                    'receipt_number': f'REC{i+1}',
                    'date': '01/01/2023',
                    'total_amount': 500.00 + i*50
                }
            })
            
        return training_examples
    
    def collect_custom_pdf_data(self):
        """Collect data from custom PDFs"""
        
        logger.info("Collecting custom PDF data...")
        
        custom_pdf_file = os.path.join(self.processed_dir, "custom_pdf_data.json")
        
        if os.path.exists(custom_pdf_file):
            with open(custom_pdf_file, 'r', encoding='utf-8') as f:
                custom_data = json.load(f)
            
            logger.info(f"Loaded {len(custom_data)} custom PDF documents")
            
            # Process custom PDF data for training
            processed_training_data = []
            
            for doc in custom_data:
                # Convert PDF data to training format
                training_example = {
                    'id': f"custom_pdf_{doc['filename']}",
                    'text': doc['text'],
                    'document_type': doc['document_type'],
                    'entities': doc['entities'],
                    'financial_data': doc.get('financial_data', {}),
                    'source': 'custom_pdf'
                }
                
                # Add to appropriate training datasets based on document type
                if doc['document_type'] == 'financial_statement' and doc.get('financial_data'):
                    # Add to financial analysis training data
                    financial_example = self._convert_pdf_to_financial_training(doc)
                    if financial_example:
                        processed_training_data.append(financial_example)
                
                elif doc['document_type'] in ['compliance_document', 'regulatory_filing']:
                    # Add to compliance training data
                    compliance_example = self._convert_pdf_to_compliance_training(doc)
                    if compliance_example:
                        processed_training_data.append(compliance_example)
                
                # Always add to document intelligence training
                processed_training_data.append(training_example)
            
            # Save processed custom PDF training data
            self._save_data(processed_training_data, "custom_pdf_training_data.json")
            
            return custom_data
        else:
            logger.info("No custom PDF data found. Run 'python scripts/process_custom_pdfs.py' to process your PDFs.")
            return []
    
    def _convert_pdf_to_financial_training(self, pdf_doc):
        """Convert PDF financial data to training format"""
        
        financial_data = pdf_doc.get('financial_data', {})
        entities = pdf_doc.get('entities', {})
        
        if not financial_data:
            return None
        
        # Calculate ratios if we have the data
        revenue = financial_data.get('revenue', 0)
        profit = financial_data.get('profit', 0)
        assets = financial_data.get('assets', 0)
        liabilities = financial_data.get('liabilities', 0)
        
        if revenue == 0 or assets == 0:
            return None
        
        # Calculate basic ratios
        profit_margin = (profit / revenue) if revenue > 0 else 0
        return_on_assets = (profit / assets) if assets > 0 else 0
        debt_to_assets = (liabilities / assets) if assets > 0 else 0
        
        # Determine risk level based on ratios
        risk_score = 100
        if profit_margin < 0:
            risk_score -= 40
        elif profit_margin < 0.05:
            risk_score -= 20
        
        if return_on_assets < 0:
            risk_score -= 20
        
        if debt_to_assets > 0.8:
            risk_score -= 25
        
        # Classify risk level
        if risk_score >= 80:
            risk_level = 0  # Low
        elif risk_score >= 60:
            risk_level = 1  # Medium
        elif risk_score >= 40:
            risk_level = 2  # High
        else:
            risk_level = 3  # Critical
        
        return {
            'id': f"pdf_financial_{pdf_doc['filename']}",
            'financial_data': financial_data,
            'ratios': {
                'profit_margin': profit_margin,
                'return_on_assets': return_on_assets,
                'debt_to_assets': debt_to_assets
            },
            'risk_level': risk_level,
            'risk_score': risk_score,
            'source': 'custom_pdf',
            'document_type': 'financial_analysis'
        }
    
    def _convert_pdf_to_compliance_training(self, pdf_doc):
        """Convert PDF compliance data to training format"""
        
        entities = pdf_doc.get('entities', {})
        
        # Extract company information
        rc_number = entities.get('rc_number')
        tin_number = entities.get('tin_number')
        
        if not rc_number and not tin_number:
            return None
        
        # Determine potential violations based on document content
        violations = []
        text_lower = pdf_doc.get('text', '').lower()
        
        if 'non-compliance' in text_lower or 'violation' in text_lower:
            if 'frc' in text_lower:
                violations.append('FRC')
            if 'firs' in text_lower or 'tax' in text_lower:
                violations.append('FIRS')
            if 'cama' in text_lower:
                violations.append('CAMA')
        
        return {
            'id': f"pdf_compliance_{pdf_doc['filename']}",
            'rc_number': rc_number,
            'tin_number': tin_number,
            'violations': violations,
            'source': 'custom_pdf',
            'document_type': 'compliance'
        }
    
    def collect_financial_statements(self) -> List[Dict]:
        """Collect financial statements for training"""
        
        # Load from files if they exist
        financial_data_file = os.path.join(self.training_dir, "financial_training_data.json")
        
        if os.path.exists(financial_data_file):
            with open(financial_data_file, 'r') as f:
                return json.load(f)
        else:
            # Generate if not exists
            data = self._generate_financial_training_data()
            self._save_data(data, "financial_training_data.json")
            return data
    
    def collect_compliance_data(self) -> List[Dict]:
        """Collect compliance data for training"""
        
        compliance_data_file = os.path.join(self.training_dir, "compliance_training_data.json")
        
        if os.path.exists(compliance_data_file):
            with open(compliance_data_file, 'r') as f:
                return json.load(f)
        else:
            data = self._generate_compliance_training_data()
            self._save_data(data, "compliance_training_data.json")
            return data

    def collect_trial_balance_data(self) -> List[Dict]:
        """Collect trial balance data for training"""
        
        trial_balance_data_file = os.path.join(self.training_dir, "trial_balance_training_data.json")
        
        if os.path.exists(trial_balance_data_file):
            with open(trial_balance_data_file, 'r') as f:
                return json.load(f)
        else:
            data = self._generate_trial_balance_training_data()
            self._save_data(data, "trial_balance_training_data.json")
            return data

    def collect_document_intelligence_data(self) -> List[Dict]:
        """Collect document intelligence data for training"""
        
        document_intelligence_data_file = os.path.join(self.training_dir, "document_intelligence_training_data.json")
        
        if os.path.exists(document_intelligence_data_file):
            with open(document_intelligence_data_file, 'r') as f:
                return json.load(f)
        else:
            data = self._generate_document_intelligence_training_data()
            self._save_data(data, "document_intelligence_training_data.json")
            return data
    
    def prepare_training_datasets(self):
        """Prepare datasets for ML training"""
        
        logger.info("Preparing training datasets...")
        
        # Financial analysis dataset
        financial_data = self.collect_financial_statements()
        financial_df = pd.DataFrame(financial_data)
        financial_df.to_csv(os.path.join(self.training_dir, "financial_analysis_dataset.csv"), index=False)
        
        # Compliance dataset
        compliance_data = self.collect_compliance_data()
        compliance_df = pd.DataFrame(compliance_data)
        compliance_df.to_csv(os.path.join(self.training_dir, "compliance_dataset.csv"), index=False)
        
        # Risk assessment dataset
        risk_data = self._generate_risk_training_data()
        risk_df = pd.DataFrame(risk_data)
        risk_df.to_csv(os.path.join(self.training_dir, "risk_assessment_dataset.csv"), index=False)

        # Trial balance classification dataset
        trial_balance_data = self.collect_trial_balance_data()
        trial_balance_df = pd.DataFrame(trial_balance_data)
        trial_balance_df.to_csv(os.path.join(self.training_dir, "trial_balance_classification_dataset.csv"), index=False)

        # Document intelligence dataset
        document_intelligence_data = self.collect_document_intelligence_data()
        document_intelligence_df = pd.DataFrame(document_intelligence_data)
        document_intelligence_df.to_csv(os.path.join(self.training_dir, "document_intelligence_dataset.csv"), index=False)
        
        logger.info("Training datasets prepared and saved")
    
    def _save_data(self, data: Any, filename: str, directory: str = None):
        """Save data to a directory"""
        if directory is None:
            directory = self.training_dir
        
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Saved {len(data) if isinstance(data, list) else 1} records to {filename}")
