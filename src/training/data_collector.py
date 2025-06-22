import logging
import os
import json
import pandas as pd
from typing import Dict, List, Any
import asyncio
from ..scrapers.ngx_scraper import NGXScraper
from ..scrapers.frc_scraper import FRCScraper

logger = logging.getLogger(__name__)

class TrainingDataCollector:
    """Collect and prepare training data for Nigerian audit AI models"""
    
    def __init__(self):
        self.data_dir = "data"
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        self.training_dir = os.path.join(self.data_dir, "training")
        
        # Create directories
        for dir_path in [self.raw_dir, self.processed_dir, self.training_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    async def collect_all_data(self):
        """Collect all training data from various sources"""
        
        logger.info("Starting comprehensive training data collection...")
        
        # Collect from scrapers
        await self._collect_from_scrapers()
        
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
        
        logger.info("Training datasets prepared and saved")
    
    def _save_data(self, data: Any, filename: str):
        """Save data to training directory"""
        
        filepath = os.path.join(self.training_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Saved {len(data) if isinstance(data, list) else 1} records to {filename}")
