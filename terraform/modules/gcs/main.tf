resource "google_storage_bucket" "sales_artifacts" {
  name                        = var.bucket_name
  location                    = var.location
  force_destroy               = false
  uniform_bucket_level_access = true
}
