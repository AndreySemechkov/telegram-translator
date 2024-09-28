# NOTICE- its not possible to use variables in this file, hence they are hardcoded.

terraform {
  backend "s3" {
    bucket         = "terraform-state-ironwatchers-prod"
    key            = "custom_api_gateway"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-ironwatchers-prod-custom_api_gateway"
  }
}
