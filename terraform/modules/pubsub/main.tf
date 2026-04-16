resource "google_pubsub_topic" "sales_events" {
  name = var.topic_name
}

resource "google_pubsub_subscription" "sales_events_sub" {
  name  = var.subscription
  topic = google_pubsub_topic.sales_events.name
}
