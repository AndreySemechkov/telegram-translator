variable "domain_name" {
  type    = string
  default = null
}

variable "root_domain" {
  type    = string
  default = "ironwatchers.com"
}

variable "aws_account" {
  type        = string
  description = "AWS account name"
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