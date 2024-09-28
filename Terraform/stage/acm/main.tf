module "acm" {
  source = "../../modules/acm"

  domain_name               = "stage-app.ironwatchers.com"
  subject_alternative_names = ["stage-app.ironwatchers.com", "stage-api.ironwatchers.com"]
  aws_region                = "us-east-1"
}