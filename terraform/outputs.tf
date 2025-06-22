utput "api_url" {
  description = "URL of the deployed API"
  value       = google_cloud_run_service.audit_ai_api.status[0].url
}

output "storage_bucket" {
  description = "Name of the storage bucket"
  value       = google_storage_bucket.audit_ai_bucket.name
}

output "bigquery_dataset" {
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.audit_dataset.dataset_id
}

output "service_account_email" {
  description = "Service account email"
  value       = google_service_account.audit_ai_sa.email
}

output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}
