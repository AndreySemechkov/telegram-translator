module "acm" {
  source = "../../modules/acm"

  domain_name               = "dev-app.ironwatchers.com"
  subject_alternative_names = ["dev-app.ironwatchers.com", "dev-api.ironwatchers.com"]
  aws_region                = "us-east-1"
}