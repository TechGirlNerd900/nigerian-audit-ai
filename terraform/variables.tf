variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "db_tier" {
  description = "Cloud SQL instance tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_user" {
  description = "Database username"
  type        = string
  default     = "audit_ai_user"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "api_key" {
  description = "API authentication key"
  type        = string
  sensitive   = true
}

variable "jwt_secret" {
  description = "JWT secret key"
  type        = string
  sensitive   = true
}

variable "allow_public_access" {
  description = "Allow public access to Cloud Run service"
  type        = bool
  default     = true
}

variable "create_notebook" {
  description = "Create Vertex AI notebook instance"
  type        = bool
  default     = false
}

variable "setup_cicd" {
  description = "Setup CI/CD with Cloud Build"
  type        = bool
  default     = false
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
  default     = ""
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "nigerian-audit-ai"
}

variable "notification_channels" {
  description = "List of notification channel IDs for monitoring alerts"
  type        = list(string)
  default     = []
}

variable "firs_api_key" {
  description = "FIRS API key for tax validation"
  type        = string
  sensitive   = true
  default     = ""
}

variable "cac_api_key" {
  description = "CAC API key for company validation"
  type        = string
  sensitive   = true
  default     = ""
}

variable "ngx_api_key" {
  description = "NGX API key for market data"
  type        = string
  sensitive   = true
  default     = ""
}

variable "enable_ssl" {
  description = "Enable SSL for database connections"
  type        = bool
  default     = true
}

variable "max_instances" {
  description = "Maximum number of Cloud Run instances"
  type        = number
  default     = 10
}

variable "min_instances" {
  description = "Minimum number of Cloud Run instances"
  type        = number
  default     = 1
}

variable "memory_limit" {
  description = "Memory limit for Cloud Run instances"
  type        = string
  default     = "4Gi"
}

variable "cpu_limit" {
  description = "CPU limit for Cloud Run instances"
  type        = string
  default     = "2000m"
}

variable "backup_retention_days" {
  description = "Number of days to retain database backups"
  type        = number
  default     = 7
}

variable "storage_class" {
  description = "Storage class for GCS bucket"
  type        = string
  default     = "STANDARD"
}

variable "enable_monitoring" {
  description = "Enable Cloud Monitoring alerts"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Log retention period in days"
  type        = number
  default     = 30
}

variable "enable_audit_logs" {
  description = "Enable audit logging"
  type        = bool
  default     = true
}

variable "custom_domain" {
  description = "Custom domain for the API"
  type        = string
  default     = ""
}

variable "ssl_certificate" {
  description = "SSL certificate for custom domain"
  type        = string
  default     = ""
}

variable "rate_limit" {
  description = "API rate limit per minute"
  type        = number
  default     = 100
}

variable "enable_redis" {
  description = "Enable Redis for caching"
  type        = bool
  default     = true
}

variable "redis_memory_size" {
  description = "Redis memory size in GB"
  type        = number
  default     = 1
}

variable "enable_vpc" {
  description = "Enable VPC for private networking"
  type        = bool
  default     = false
}

variable "authorized_networks" {
  description = "List of authorized networks for database access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "enable_point_in_time_recovery" {
  description = "Enable point-in-time recovery for database"
  type        = bool
  default     = true
}

variable "deletion_protection" {
  description = "Enable deletion protection for critical resources"
  type        = bool
  default     = true
}

variable "labels" {
  description = "Common labels to apply to all resources"
  type        = map(string)
  default = {
    project     = "nigerian-audit-ai"
    managed-by  = "terraform"
    environment = "production"
  }
}