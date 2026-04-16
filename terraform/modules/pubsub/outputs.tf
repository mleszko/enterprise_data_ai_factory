output "topic_name" {
  value = google_pubsub_topic.sales_events.name
}

output "subscription_name" {
  value = google_pubsub_subscription.sales_events_sub.name
}
