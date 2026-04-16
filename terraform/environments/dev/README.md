# terraform/environments/dev/

Development environment variables for Terraform runs.

## Files

- `terraform.tfvars.example`: example values to bootstrap a dev deployment.

## Usage

1. Copy the example:
   - `cp terraform/environments/dev/terraform.tfvars.example terraform/environments/dev/terraform.tfvars`
2. Fill real `project_id` and globally unique `gcs_bucket_name`.
3. Run from `terraform/` with:
   - `terraform plan -var-file=environments/dev/terraform.tfvars`
