import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import logging
from typing import Tuple, Dict, List
from google.cloud import storage
from ..config.settings import settings
from ..training.data_collector import TrainingDataCollector

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.data_collector = TrainingDataCollector()
        
    def prepare_financial_analysis_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for financial analysis model"""
        
        # Collect training data
        financial_data = self.data_collector.collect_financial_statements()
        
        # Features: financial ratios
        features = []
        labels = []
        
        for record in financial_data:
            # Extract financial ratios as features
            feature_vector = [
                record.get('current_ratio', 0),
                record.get('quick_ratio', 0),
                record.get('debt_to_equity', 0),
                record.get('debt_to_assets', 0),
                record.get('gross_profit_margin', 0),
                record.get('net_profit_margin', 0),
                record.get('return_on_assets', 0),
                record.get('return_on_equity', 0),
                record.get('asset_turnover', 0),
                record.get('inventory_turnover', 0),
                # Add more features...
            ]
            
            # Risk level as label (0: Low, 1: Medium, 2: High, 3: Critical)
            risk_label = record.get('risk_level', 0)
            
            features.append(feature_vector)
            labels.append(risk_label)
        
        return np.array(features), np.array(labels)
    
    def train_financial_analysis_model(self) -> keras.Model:
        """Train financial analysis neural network"""
        
        logger.info("Training financial analysis model...")
        
        # Prepare data
        X, y = self.prepare_financial_analysis_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Store scaler
        self.scalers['financial_analysis'] = scaler
        
        # Convert to categorical
        y_train_cat = keras.utils.to_categorical(y_train, num_classes=4)
        y_test_cat = keras.utils.to_categorical(y_test, num_classes=4)
        
        # Build model
        model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(4, activation='softmax')  # 4 risk levels
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=settings.LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Add callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5),
            keras.callbacks.ModelCheckpoint(
                'models/checkpoints/financial_analysis_best.h5',
                save_best_only=True
            )
        ]
        
        # Train model
        history = model.fit(
            X_train_scaled, y_train_cat,
            epochs=100,
            batch_size=settings.TRAINING_BATCH_SIZE,
            validation_data=(X_test_scaled, y_test_cat),
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        y_pred_classes = np.argmax(y_pred, axis=1)
        
        logger.info("Classification Report:")
        logger.info(classification_report(y_test, y_pred_classes))
        
        # Store model
        self.models['financial_analysis'] = model
        
        return model
    
    def train_compliance_checker_model(self) -> keras.Model:
        """Train compliance checking model"""
        
        logger.info("Training compliance checker model...")
        
        # Collect compliance training data
        compliance_data = self.data_collector.collect_compliance_data()
        
        # Prepare features
        features = []
        labels = []
        
        for record in compliance_data:
            # Company features
            feature_vector = [
                record.get('company_size', 0),  # Encoded: 0=small, 1=medium, 2=large
                record.get('industry_type', 0),  # Encoded industry
                record.get('is_public', 0),  # 0/1
                record.get('annual_revenue', 0),  # Normalized
                record.get('total_assets', 0),  # Normalized
                record.get('employee_count', 0),  # Normalized
                # Add more features...
            ]
            
            # Compliance violations as multi-label
            violations = record.get('violations', [])
            label_vector = [
                1 if 'FRC' in violations else 0,
                1 if 'FIRS' in violations else 0,
                1 if 'CAMA' in violations else 0,
                1 if 'CBN' in violations else 0,
                # Add more compliance categories...
            ]
            
            features.append(feature_vector)
            labels.append(label_vector)
        
        X = np.array(features)
        y = np.array(labels)
        
        # Split and scale
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        self.scalers['compliance'] = scaler
        
        # Build multi-label classification model
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(y.shape[1], activation='sigmoid')  # Multi-label output
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Train model
        history = model.fit(
            X_train_scaled, y_train,
            epochs=50,
            batch_size=32,
            validation_data=(X_test_scaled, y_test),
            verbose=1
        )
        
        self.models['compliance'] = model
        return model
    
    def train_risk_assessment_model(self) -> keras.Model:
        """Train risk assessment model"""
        
        logger.info("Training risk assessment model...")
        
        # Similar structure to other models...
        # Implementation would include:
        # - Risk factor extraction
        # - Historical loss data
        # - Industry risk patterns
        # - Regulatory risk indicators
        
        pass  # Placeholder for now
    
    def save_models_to_gcs(self):
        """Save trained models to Google Cloud Storage"""
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(settings.GCS_BUCKET)
        
        for model_name, model in self.models.items():
            # Save model
            model_path = f"models/{model_name}/{settings.MODEL_VERSION}"
            model.save(f"temp_{model_name}")
            
            # Upload to GCS
            blob = bucket.blob(f"{model_path}/model.h5")
            blob.upload_from_filename(f"temp_{model_name}")
            
            logger.info(f"Uploaded {model_name} model to GCS")
        
        # Save scalers
        for scaler_name, scaler in self.scalers.items():
            joblib.dump(scaler, f"temp_scaler_{scaler_name}.pkl")
            blob = bucket.blob(f"models/{scaler_name}/scaler.pkl")
            blob.upload_from_filename(f"temp_scaler_{scaler_name}.pkl")
    
    def train_all_models(self):
        """Train all models in sequence"""
        
        logger.info("Starting model training pipeline...")
        
        # Train models
        self.train_financial_analysis_model()
        self.train_compliance_checker_model()
        # self.train_risk_assessment_model()
        
        # Save to GCS
        self.save_models_to_gcs()
        
        logger.info("Model training pipeline completed!")

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_all_models()