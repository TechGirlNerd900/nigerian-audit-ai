from google.cloud import aiplatform
import os
import logging

logger = logging.getLogger(__name__)

def deploy_model_to_endpoint(model_name: str, model_id: str):
    """Deploy trained model to Vertex AI endpoint"""
    
    # Initialize Vertex AI
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GCP_REGION", "us-central1")
    )
    
    # Get the model
    model = aiplatform.Model(model_name=model_id)
    
    # Create endpoint
    endpoint = aiplatform.Endpoint.create(
        display_name=f"nigerian-audit-{model_name}-endpoint",
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GCP_REGION", "us-central1")
    )
    
    # Deploy model to endpoint
    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=f"{model_name}-v1",
        machine_type="n1-standard-4",
        min_replica_count=1,
        max_replica_count=3,
        accelerator_type=None,  # Use CPU for inference
        accelerator_count=0,
    )
    
    logger.info(f"Model {model_name} deployed to endpoint: {endpoint.resource_name}")
    return endpoint

def main():
    # Deploy all trained models
    models_to_deploy = [
        ("financial_analysis", "projects/PROJECT_ID/locations/us-central1/models/MODEL_ID"),
        ("compliance_checker", "projects/PROJECT_ID/locations/us-central1/models/MODEL_ID"),
        ("risk_assessment", "projects/PROJECT_ID/locations/us-central1/models/MODEL_ID"),
    ]
    
    for model_name, model_id in models_to_deploy:
        deploy_model_to_endpoint(model_name, model_id)

if __name__ == "__main__":
    main()