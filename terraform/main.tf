terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "sales_pubsub" {
  source       = "./modules/pubsub"
  topic_name   = var.pubsub_topic_name
  subscription = var.pubsub_subscription_name
}

module "sales_gcs" {
  source      = "./modules/gcs"
  bucket_name = var.gcs_bucket_name
  location    = var.region
}
