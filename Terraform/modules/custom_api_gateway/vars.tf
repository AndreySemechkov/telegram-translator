variable "certificate_name" {
  type    = string
  default = null
  description = "ACM certificate name"
}

variable "api_gateway_dns" {
  type    = string
  default = null
}

variable "root_domain" {
  type    = string
  default = "ironwatchers.com"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}