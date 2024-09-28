module "acm" {
  source = "../../modules/acm"

  domain_name               = "app.ironwatchers.com"
  subject_alternative_names = ["app.ironwatchers.com", "api.ironwatchers.com"]
  aws_region                = "us-east-1"
}
