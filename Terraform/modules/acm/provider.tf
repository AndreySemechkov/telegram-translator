provider "aws" {
  region = var.aws_region
}

# Used for Route53 management in our central account.
provider "aws" {
  alias   = "mgmt_account"
  region  = "us-east-1"
  profile = "iron-mgmt"
}

terraform {
  required_providers {
    aws = {
      version = "~> 5.21.0"
    }
  }
}
