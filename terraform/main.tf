terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.84"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "storage.googleapis.com",
    "bigquery.googleapis.com",
    "documentai.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "compute.googleapis.com",
    "containerregistry.googleapis.com"
  ])

  project = var.project_id
  service = each.value

  disable_dependent_services = true
}

# Service Account for the application
resource "google_service_account" "audit_ai_sa" {
  account_id   = "nigerian-audit-ai"
  display_name = "Nigerian Audit AI Service Account"
  description  = "Service account for Nigerian Audit AI application"
}

# IAM roles for the service account
resource "google_project_iam_member" "audit_ai_permissions" {
  for_each = toset([
    "roles/aiplatform.admin",
    "roles/storage.admin",
    "roles/bigquery.admin",
    "roles/documentai.apiUser",
    "roles/cloudbuild.builds.editor",
    "roles/run.admin"
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.audit_ai_sa.email}"
}

# Cloud Storage bucket for models and data
resource "google_storage_bucket" "audit_ai_bucket" {
  name          = "${var.project_id}-nigerian-audit-ai"
  location      = var.region
  force_destroy = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# BigQuery dataset for training and analytics
resource "google_bigquery_dataset" "audit_dataset" {
  dataset_id  = "nigerian_audit_ai"
  description = "Dataset for Nigerian Audit AI training and analytics"
  location    = var.region

  access {
    role          = "OWNER"
    user_by_email = google_service_account.audit_ai_sa.email
  }

  labels = {
    environment = var.environment
    project     = "nigerian-audit-ai"
  }
}

# BigQuery tables
resource "google_bigquery_table" "companies" {
  dataset_id = google_bigquery_dataset.audit_dataset.dataset_id
  table_id   = "companies"

  schema = jsonencode([
    {
      name = "id"
      type = "INTEGER"
      mode = "REQUIRED"
    },
    {
      name = "name"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "cac_number"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "tin_number"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "industry"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "created_at"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    }
  ])

  deletion_protection = false
}

resource "google_bigquery_table" "audit_logs" {
  dataset_id = google_bigquery_dataset.audit_dataset.dataset_id
  table_id   = "audit_logs"

  schema = jsonencode([
    {
      name = "id"
      type = "INTEGER"
      mode = "REQUIRED"
    },
    {
      name = "action"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "user_id"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "company_id"
      type = "INTEGER"
      mode = "NULLABLE"
    },
    {
      name = "details"
      type = "JSON"
      mode = "NULLABLE"
    },
    {
      name = "timestamp"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    }
  ])

  deletion_protection = false
}

# Cloud SQL instance for PostgreSQL
resource "google_sql_database_instance" "audit_ai_db" {
  name             = "nigerian-audit-ai-db"
  database_version = "POSTGRES_15"
  region          = var.region
  deletion_protection = false

  settings {
    tier              = var.db_tier
    availability_type = "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = 20

    database_flags {
      name  = "log_checkpoints"
      value = "on"
    }

    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 7
      }
    }

    ip_configuration {
      ipv4_enabled    = true
      authorized_networks {
        value = "0.0.0.0/0"
        name  = "all"
      }
    }
  }
}

# Database
resource "google_sql_database" "audit_ai_database" {
  name     = "nigerian_audit_ai"
  instance = google_sql_database_instance.audit_ai_db.name
}

# Database user
resource "google_sql_user" "audit_ai_user" {
  name     = var.db_user
  instance = google_sql_database_instance.audit_ai_db.name
  password = var.db_password
}

# Cloud Run service
resource "google_cloud_run_service" "audit_ai_api" {
  name     = "nigerian-audit-ai-api"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.audit_ai_sa.email
      
      containers {
        image = "gcr.io/${var.project_id}/nigerian-audit-ai:latest"
        
        resources {
          limits = {
            cpu    = "2000m"
            memory = "4Gi"
          }
        }

        env {
          name  = "GOOGLE_CLOUD_PROJECT_ID"
          value = var.project_id
        }

        env {
          name  = "GCP_REGION"
          value = var.region
        }

        env {
          name  = "GCS_BUCKET"
          value = google_storage_bucket.audit_ai_bucket.name
        }

        env {
          name  = "DATABASE_URL"
          value = "postgresql://${var.db_user}:${var.db_password}@${google_sql_database_instance.audit_ai_db.public_ip_address}:5432/nigerian_audit_ai"
        }

        env {
          name  = "API_KEY"
          value = var.api_key
        }

        env {
          name  = "JWT_SECRET"
          value = var.jwt_secret
        }

        ports {
          container_port = 8000
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "10"
        "run.googleapis.com/cpu-throttling" = "false"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.apis]
}

# Cloud Run IAM
resource "google_cloud_run_service_iam_member" "public_access" {
  count = var.allow_public_access ? 1 : 0
  
  service  = google_cloud_run_service.audit_ai_api.name
  location = google_cloud_run_service.audit_ai_api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Vertex AI notebook instance for model development
resource "google_notebooks_instance" "audit_ai_notebook" {
  count = var.create_notebook ? 1 : 0
  
  name         = "nigerian-audit-ai-notebook"
  location     = "${var.region}-a"
  machine_type = "n1-standard-4"

  vm_image {
    project      = "deeplearning-platform-release"
    image_family = "tf-ent-2-11-cu113-notebooks"
  }

  service_account = google_service_account.audit_ai_sa.email

  labels = {
    environment = var.environment
    project     = "nigerian-audit-ai"
  }
}

# Cloud Build trigger for CI/CD
resource "google_cloudbuild_trigger" "audit_ai_trigger" {
  count = var.setup_cicd ? 1 : 0
  
  name        = "nigerian-audit-ai-build"
  description = "Build and deploy Nigerian Audit AI"

  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "^main$"
    }
  }

  filename = "cloudbuild.yaml"

  substitutions = {
    _PROJECT_ID = var.project_id
    _REGION     = var.region
  }
}

# Cloud Monitoring alert policy
resource "google_monitoring_alert_policy" "high_error_rate" {
  display_name = "Nigerian Audit AI - High Error Rate"
  combiner     = "OR"

  conditions {
    display_name = "Error rate too high"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"nigerian-audit-ai-api\""
      duration        = "300s"
      comparison      = "COMPARISON_GREATER_THAN"
      threshold_value = 0.1

      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = var.notification_channels

  alert_strategy {
    auto_close = "86400s"
  }
}

# Secret Manager secrets
resource "google_secret_manager_secret" "api_key" {
  secret_id = "nigerian-audit-ai-api-key"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "api_key_version" {
  secret      = google_secret_manager_secret.api_key.id
  secret_data = var.api_key
}

resource "google_secret_manager_secret" "jwt_secret" {
  secret_id = "nigerian-audit-ai-jwt-secret"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "jwt_secret_version" {
  secret      = google_secret_manager_secret.jwt_secret.id
  secret_data = var.jwt_secret
}