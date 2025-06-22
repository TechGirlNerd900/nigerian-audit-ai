"""
Database setup script for Nigerian Audit AI
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

# Database Models
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cac_number = Column(String(20), unique=True, index=True)
    tin_number = Column(String(12), index=True)
    business_type = Column(String(100))
    industry = Column(String(100))
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class FinancialStatement(Base):
    __tablename__ = "financial_statements"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    financial_year = Column(String(10))
    revenue = Column(Float)
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    net_income = Column(Float)
    trial_balance = Column(JSON)
    ratios = Column(JSON)
    created_at = Column(DateTime)

class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    regulation_type = Column(String(50))
    status = Column(String(50))
    score = Column(Float)
    violations = Column(JSON)
    check_date = Column(DateTime)
    created_at = Column(DateTime)

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    overall_risk_score = Column(Float)
    risk_level = Column(String(20))
    risk_components = Column(JSON)
    assessment_date = Column(DateTime)
    created_at = Column(DateTime)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100))
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    user_id = Column(String(100))
    details = Column(JSON)
    timestamp = Column(DateTime)

def create_database():
    """Create database and tables"""
    
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Database tables created successfully")
        
        # Test connection
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Test query
        result = session.execute("SELECT 1").fetchone()
        session.close()
        
        logger.info("✅ Database connection test successful")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

def seed_sample_data():
    """Insert sample data for testing"""
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Sample companies
        companies = [
            Company(
                name="Dangote Cement Plc",
                cac_number="RC123456",
                tin_number="123456789012",
                business_type="Public Limited Company",
                industry="Manufacturing",
                is_public=True
            ),
            Company(
                name="MTN Nigeria Communications Plc",
                cac_number="RC789012",
                tin_number="789012345678",
                business_type="Public Limited Company", 
                industry="Telecommunications",
                is_public=True
            )
        ]
        
        session.add_all(companies)
        session.commit()
        
        logger.info("✅ Sample data inserted successfully")
        session.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to insert sample data: {e}")
        return False

def main():
    """Main setup function"""
    
    logger.info("🇳🇬 Starting Nigerian Audit AI Database Setup...")
    
    # Create database
    if create_database():
        logger.info("Database created successfully")
        
        # Seed sample data
        if seed_sample_data():
            logger.info("Sample data inserted")
        
        logger.info("✅ Database setup completed successfully!")
        return True
    else:
        logger.error("❌ Database setup failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
