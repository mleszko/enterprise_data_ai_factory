output "pubsub_topic" {
  value = module.sales_pubsub.topic_name
}

output "pubsub_subscription" {
  value = module.sales_pubsub.subscription_name
}

output "gcs_bucket" {
  value = module.sales_gcs.bucket_name
}
