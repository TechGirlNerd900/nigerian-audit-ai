import sys
import os
import argparse
import logging
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.training.model_trainer import ModelTrainer
from src.training.data_collector import TrainingDataCollector
from src.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Train Nigerian Audit AI Models")
    parser.add_argument(
        "--model",
        choices=["all", "financial", "compliance", "risk", "document"],
        default="all",
        help="Which model to train"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Training batch size"
    )
    parser.add_argument(
        "--collect-data",
        action="store_true",
        help="Collect fresh training data before training"
    )
    parser.add_argument(
        "--vertex",
        action="store_true",
        help="Train on Vertex AI"
    )
    
    args = parser.parse_args()
    
    logger.info("🇳🇬 Starting Nigerian Audit AI Model Training")
    logger.info(f"Model: {args.model}")
    logger.info(f"Epochs: {args.epochs}")
    logger.info(f"Batch Size: {args.batch_size}")
    logger.info(f"Train on Vertex AI: {args.vertex}")
    
    # Collect data if requested
    if args.collect_data:
        logger.info("📊 Collecting training data...")
        collector = TrainingDataCollector()
        collector.collect_all_data()
    
    # Initialize trainer
    trainer = ModelTrainer(train_on_vertex=args.vertex)
    
    # Train models
    if args.model == "all":
        trainer.train_all_models(epochs=args.epochs, batch_size=args.batch_size)
    elif args.model == "financial":
        trainer.train_financial_analysis_model(epochs=args.epochs, batch_size=args.batch_size)
    elif args.model == "compliance":
        trainer.train_compliance_checker_model()
    elif args.model == "risk":
        trainer.train_risk_assessment_model()
    elif args.model == "document":
        trainer.train_document_processor_model()
    
    logger.info("✅ Model training completed!")

if __name__ == "__main__":
    main()
