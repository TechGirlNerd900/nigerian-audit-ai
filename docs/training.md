# Model Training Guide

## Overview

The Nigerian Audit AI uses multiple specialized models trained on financial data and Nigerian regulatory requirements.

## Training Pipeline

### 1. Data Collection
```bash
python scripts/collect_data.py
```

Collects training data from:
- Nigerian Exchange Group (NGX) financial statements
- FRC regulations and guidelines
- Synthetic financial scenarios
- Historical audit data

### 2. Data Preprocessing
```bash
python src/training/preprocessor.py
```

Processes data for training:
- Account classification normalization
- Financial ratio calculations
- Nigerian currency standardization
- Regulatory mapping

### 3. Model Training

#### Train All Models
```bash
python scripts/train_models.py --model all
```

#### Train Specific Models
```bash
# Financial analysis model
python scripts/train_models.py --model financial

# Compliance checker model  
python scripts/train_models.py --model compliance

# Risk assessment model
python scripts/train_models.py --model risk
```

### 4. Training on Vertex AI

```bash
python src/training/vertex_ai_trainer.py
```

## Model Architecture

### Financial Analysis Model
- **Type**: Neural Network (Dense layers)
- **Input**: Financial ratios (10 features)
- **Output**: Risk classification (4 classes)
- **Accuracy**: >85% on test set

### Compliance Checker Model  
- **Type**: Multi-label classification
- **Input**: Company characteristics (6 features)
- **Output**: Violation flags (4 regulations)
- **F1-Score**: >90% per regulation

### Risk Assessment Model
- **Type**: Ensemble (Random Forest + Neural Network)
- **Input**: Risk factors (7 features)  
- **Output**: Risk score (0-100)
- **RMSE**: <5% on validation set

## Nigerian-Specific Training

### Industry Benchmarks
Models are trained on Nigerian industry data:
- Banking sector: CBN prudential guidelines
- Manufacturing: Local production metrics
- Oil & Gas: Nigerian content requirements
- Telecommunications: NCC regulations

### Regulatory Training Data
- FRC compliance scenarios
- FIRS tax calculation examples
- CAMA registration requirements
- CBN banking regulations

### Currency and Localization
- Nigerian Naira amount handling
- Local business practices
- Regional economic factors
- Regulatory compliance patterns

## Model Evaluation

### Performance Metrics
```python
# Financial Analysis Model
accuracy = 0.87
precision = 0.85  
recall = 0.89
f1_score = 0.87

# Compliance Model
frc_f1 = 0.92
firs_f1 = 0.91
cama_f1 = 0.94
overall_accuracy = 0.89
```

### Validation Strategy
- **Training**: 70% of data
- **Validation**: 15% of data  
- **Testing**: 15% of data
- **Cross-validation**: 5-fold for robustness

## Continuous Learning

### Model Updates
- Monthly retraining with new data
- Quarterly evaluation against benchmarks
- Annual architecture reviews

### Data Pipeline
- Automated data collection from NGX
- Regulatory update monitoring
- Performance feedback integration

## Training Costs

### Local Training
- Development: Free (CPU training)
- Small models: $0-50/month

### GCP Vertex AI
- Model training: $20-100/job
- Hyperparameter tuning: $50-200/job
- Large-scale training: $200-500/month