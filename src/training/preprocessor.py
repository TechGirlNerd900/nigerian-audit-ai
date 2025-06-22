import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
import logging
from typing import Tuple, Dict, Any
import joblib
import os

logger = logging.getLogger(__name__)

class NigerianAuditDataPreprocessor:
    """Preprocess data for Nigerian audit AI models"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.feature_columns = {}
    
    def preprocess_financial_data(self, data_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess financial analysis training data"""
        
        logger.info("Preprocessing financial analysis data...")
        
        # Load data
        df = pd.read_csv(data_path)
        
        # Extract features and labels
        feature_columns = [
            'current_ratio', 'debt_to_equity', 'profit_margin', 'return_on_assets',
            'debt_to_assets', 'gross_profit_margin', 'net_profit_margin', 
            'return_on_equity', 'asset_turnover', 'inventory_turnover'
        ]
        
        # Handle missing columns
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0  # Default value for missing features
        
        # Extract features
        X = df[feature_columns].fillna(0).values
        
        # Extract labels (risk levels)
        y = df['risk_level'].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Store scaler
        self.scalers['financial_analysis'] = scaler
        self.feature_columns['financial_analysis'] = feature_columns
        
        logger.info(f"Processed {len(X)} financial samples with {len(feature_columns)} features")
        
        return X_scaled, y
    
    def preprocess_compliance_data(self, data_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess compliance checking training data"""
        
        logger.info("Preprocessing compliance data...")
        
        # Load data
        df = pd.read_csv(data_path)
        
        # Extract features
        feature_columns = [
            'company_size', 'industry_type', 'is_public', 
            'annual_revenue', 'total_assets', 'employee_count'
        ]
        
        # Normalize revenue and assets (log transform for large values)
        df['annual_revenue_log'] = np.log1p(df['annual_revenue'])
        df['total_assets_log'] = np.log1p(df['total_assets'])
        df['employee_count_log'] = np.log1p(df['employee_count'])
        
        # Updated feature columns
        feature_columns = [
            'company_size', 'industry_type', 'is_public',
            'annual_revenue_log', 'total_assets_log', 'employee_count_log'
        ]
        
        X = df[feature_columns].fillna(0).values
        
        # Process violations (multi-label)
        violation_types = ['FRC', 'FIRS', 'CAMA', 'CBN']
        y = np.zeros((len(df), len(violation_types)))
        
        for i, violations in enumerate(df['violations']):
            if pd.notna(violations) and violations != '[]':
                # Parse violation list (stored as string)
                violation_list = eval(violations) if isinstance(violations, str) else violations
                for j, violation_type in enumerate(violation_types):
                    if violation_type in violation_list:
                        y[i, j] = 1
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Store scaler and feature info
        self.scalers['compliance'] = scaler
        self.feature_columns['compliance'] = feature_columns
        
        logger.info(f"Processed {len(X)} compliance samples with {len(feature_columns)} features")
        
        return X_scaled, y
    
    def preprocess_risk_data(self, data_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess risk assessment training data"""
        
        logger.info("Preprocessing risk assessment data...")
        
        # Load data
        df = pd.read_csv(data_path)
        
        # Extract risk component features
        risk_features = [
            'liquidity_risk', 'credit_risk', 'operational_risk', 
            'market_risk', 'regulatory_risk'
        ]
        
        # Add categorical features
        categorical_features = ['industry', 'company_size']
        
        # Encode categorical variables
        industry_encoder = LabelEncoder()
        df['industry_encoded'] = industry_encoder.fit_transform(df['industry'])
        
        size_encoder = LabelEncoder()
        df['company_size_encoded'] = size_encoder.fit_transform(df['company_size'])
        
        # Store encoders
        self.encoders['industry'] = industry_encoder
        self.encoders['company_size'] = size_encoder
        
        # Combine all features
        all_features = risk_features + ['industry_encoded', 'company_size_encoded']
        X = df[all_features].values
        
        # Extract labels
        y = df['risk_level'].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Store scaler and feature info
        self.scalers['risk_assessment'] = scaler
        self.feature_columns['risk_assessment'] = all_features
        
        logger.info(f"Processed {len(X)} risk assessment samples with {len(all_features)} features")
        
        return X_scaled, y
    
    def create_train_val_test_splits(self, X: np.ndarray, y: np.ndarray, 
                                   test_size: float = 0.2, val_size: float = 0.2,
                                   random_state: int = 42) -> Tuple[np.ndarray, ...]:
        """Create train, validation, and test splits"""
        
        # First split: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, 
            stratify=y if len(y.shape) == 1 else None
        )
        
        # Second split: train vs val
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state,
            stratify=y_temp if len(y_temp.shape) == 1 else None
        )
        
        logger.info(f"Data splits - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def save_preprocessors(self, save_dir: str = "models/preprocessors"):
        """Save all preprocessors for later use"""
        
        os.makedirs(save_dir, exist_ok=True)
        
        # Save scalers
        for name, scaler in self.scalers.items():
            joblib.dump(scaler, os.path.join(save_dir, f'{name}_scaler.pkl'))
        
        # Save encoders
        for name, encoder in self.encoders.items():
            joblib.dump(encoder, os.path.join(save_dir, f'{name}_encoder.pkl'))
        
        # Save feature column information
        joblib.dump(self.feature_columns, os.path.join(save_dir, 'feature_columns.pkl'))
        
        logger.info(f"Preprocessors saved to {save_dir}")
    
    def load_preprocessors(self, save_dir: str = "models/preprocessors"):
        """Load preprocessors from saved files"""
        
        try:
            # Load feature columns
            self.feature_columns = joblib.load(os.path.join(save_dir, 'feature_columns.pkl'))
            
            # Load scalers
            for model_name in self.feature_columns.keys():
                scaler_path = os.path.join(save_dir, f'{model_name}_scaler.pkl')
                if os.path.exists(scaler_path):
                    self.scalers[model_name] = joblib.load(scaler_path)
            
            # Load encoders
            encoder_files = [f for f in os.listdir(save_dir) if f.endswith('_encoder.pkl')]
            for encoder_file in encoder_files:
                encoder_name = encoder_file.replace('_encoder.pkl', '')
                self.encoders[encoder_name] = joblib.load(os.path.join(save_dir, encoder_file))
            
            logger.info(f"Preprocessors loaded from {save_dir}")
            
        except Exception as e:
            logger.error(f"Failed to load preprocessors: {e}")
    
    def transform_new_data(self, data: Dict[str, Any], model_type: str) -> np.ndarray:
        """Transform new data using saved preprocessors"""
        
        if model_type not in self.scalers:
            raise ValueError(f"No preprocessor found for model type: {model_type}")
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame([data])
        
        # Get feature columns for this model type
        feature_cols = self.feature_columns[model_type]
        
        # Prepare features based on model type
        if model_type == 'financial_analysis':
            X = df[feature_cols].fillna(0).values
        
        elif model_type == 'compliance':
            # Apply same transformations as during training
            df['annual_revenue_log'] = np.log1p(df['annual_revenue'])
            df['total_assets_log'] = np.log1p(df['total_assets'])
            df['employee_count_log'] = np.log1p(df['employee_count'])
            X = df[feature_cols].fillna(0).values
        
        elif model_type == 'risk_assessment':
            # Encode categorical variables
            if 'industry' in data:
                df['industry_encoded'] = self.encoders['industry'].transform([data['industry']])[0]
            if 'company_size' in data:
                df['company_size_encoded'] = self.encoders['company_size'].transform([data['company_size']])[0]
            X = df[feature_cols].fillna(0).values
        
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Apply scaling
        X_scaled = self.scalers[model_type].transform(X)
        
        return X_scaled