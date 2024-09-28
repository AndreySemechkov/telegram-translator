# NOTICE- its not possible to use variables in this file, hence they are hardcoded.

terraform {
  backend "s3" {
    bucket         = "terraform-state-ironwatchers-dev"
    key            = "cloudfront"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-ironwatchers-dev-cloudfront"
  }
}