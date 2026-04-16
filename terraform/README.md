# terraform/

Infrastructure as Code for the GCP baseline.

## Scope

- Pub/Sub topic + subscription for sales events.
- GCS bucket for raw, curated, and model artifacts.

## Structure

- `main.tf`, `variables.tf`, `outputs.tf`: root composition.
- `modules/pubsub/`: Pub/Sub resources.
- `modules/gcs/`: Storage resources.
- `environments/dev/`: example `tfvars` for dev setup.

## Typical Workflow

1. `terraform init`
2. `terraform plan -var-file=environments/dev/terraform.tfvars`
3. `terraform apply -var-file=environments/dev/terraform.tfvars`
