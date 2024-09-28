variable "bucket_name" {
  type        = string
  description = "The name of the desired S3 bucket"
  default     = null
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "aws_account_id" {
  type        = string
  description = "AWS account ID"
  default     = null
}

