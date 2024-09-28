module "cloudfront" {
  source = "../../modules/cloudfront"

  domain_name    = "stage-app.ironwatchers.com"
  aws_account    = "stage"
  aws_region     = "us-east-1"
  aws_account_id = "634882056334"
}