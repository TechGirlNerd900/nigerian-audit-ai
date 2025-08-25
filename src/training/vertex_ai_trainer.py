from google.cloud import aiplatform
from google.cloud.aiplatform import gapic as aip
import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class VertexAITrainer:
    def __init__(self, project_id: str, region: str = "us-central1"):
        self.project_id = project_id
        self.region = region
        aiplatform.init(project=project_id, location=region)
    
    def create_training_job(self, model_type: str, config: Dict):
        """Create custom training job on Vertex AI"""
        
        display_name = f"nigerian-audit-{model_type}-training"
        
        # Define container spec
        container_spec = {
            "image_uri": f"gcr.io/{self.project_id}/nigerian-audit-trainer:latest",
            "command": [],
            "args": [
                "--model-type", model_type,
                "--epochs", str(config.get("epochs", 100)),
                "--batch-size", str(config.get("batch_size", 32)),
                "--learning-rate", str(config.get("learning_rate", 0.001))
            ]
        }
        
        # Define machine spec
        machine_spec = {
            "machine_type": "n1-standard-8",
            "accelerator_type": aip.AcceleratorType.NVIDIA_TESLA_T4,
            "accelerator_count": 1,
        }
        
        # Create training job
        job = aiplatform.CustomTrainingJob(
            display_name=display_name,
            container_spec=container_spec,
            requirements=["tensorflow==2.15.0", "scikit-learn==1.3.2"],
            model_serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/tf2-cpu.2-8:latest",
        )
        
        # Submit job
        model = job.run(
            dataset=None,  # Using our custom data pipeline
            replica_count=1,
            machine_type="n1-standard-8",
            accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=1,
            base_output_dir=f"gs://{self.project_id}-nigerian-audit-ai/training-outputs",
            sync=True
        )
        
        logger.info(f"Training job completed. Model: {model.display_name}")
        return model
    
    def train_all_models(self):
        """Train all models sequentially"""
        
        models_config = {
            "financial_analysis": {
                "epochs": 100,
                "batch_size": 32,
                "learning_rate": 0.001
            },
            "compliance_checker": {
                "epochs": 50,
                "batch_size": 64,
                "learning_rate": 0.001
            },
            "risk_assessment": {
                "epochs": 75,
                "batch_size": 32,
                "learning_rate": 0.0005
            }
        }
        
        trained_models = {}
        
        for model_type, config in models_config.items():
            logger.info(f"Training {model_type} model...")
            model = self.create_training_job(model_type, config)
            trained_models[model_type] = model
        
        return trained_models

def main():
    trainer = VertexAITrainer(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        region=os.getenv("GCP_REGION", "us-central1")
    )
    
    trainer.train_all_models()

if __name__ == "__main__":
    main()
