variable "domain_name" {
  type    = string
  default = null
}

variable "root_domain" {
  type    = string
  default = "ironwatchers.com"
}

variable "subject_alternative_names" {
  type        = list(any)
  default     = null
  description = "applicable fqdns under the same ACM certificate"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}