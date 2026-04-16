variable "project_id" {
  type        = string
  description = "GCP project id"
}

variable "region" {
  type        = string
  default     = "europe-west1"
  description = "GCP region"
}

variable "pubsub_topic_name" {
  type        = string
  default     = "retail-sales-events"
  description = "Pub/Sub topic for incoming sales events"
}

variable "pubsub_subscription_name" {
  type        = string
  default     = "retail-sales-events-sub"
  description = "Subscription consumed by streaming pipeline"
}

variable "gcs_bucket_name" {
  type        = string
  description = "Bucket for raw/curated/model artifacts"
}
