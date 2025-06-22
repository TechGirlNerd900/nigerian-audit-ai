# scripts/setup_monitoring.py
from google.cloud import monitoring_v3
import time

def create_custom_metrics():
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}"
    
    # Define custom metrics
    metrics = [
        {
            "type": "custom.googleapis.com/nigerian_audit/prediction_accuracy",
            "labels": [
                {"key": "model_type", "value_type": "STRING"},
                {"key": "prediction_class", "value_type": "STRING"}
            ],
            "metric_kind": "GAUGE",
            "value_type": "DOUBLE",
            "description": "Prediction accuracy for Nigerian audit models"
        },
        {
            "type": "custom.googleapis.com/nigerian_audit/compliance_violations",
            "labels": [
                {"key": "regulation_type", "value_type": "STRING"},
                {"key": "severity", "value_type": "STRING"}
            ],
            "metric_kind": "CUMULATIVE",
            "value_type": "INT64",
            "description": "Count of compliance violations detected"
        }
    ]
    
    for metric_descriptor in metrics:
        descriptor = monitoring_v3.MetricDescriptor(
            type=metric_descriptor["type"],
            metric_kind=metric_descriptor["metric_kind"],
            value_type=metric_descriptor["value_type"],
            description=metric_descriptor["description"]
        )
        
        # Add labels
        for label in metric_descriptor["labels"]:
            descriptor.labels.append(
                monitoring_v3.LabelDescriptor(
                    key=label["key"],
                    value_type=label["value_type"]
                )
            )
        
        # Create the metric descriptor
        client.create_metric_descriptor(
            name=project_name,
            metric_descriptor=descriptor
        )

if __name__ == "__main__":
    create_custom_metrics()