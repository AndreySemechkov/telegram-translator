module "cloudfront" {
  source = "../../modules/cloudfront"

  domain_name    = "dev-app.ironwatchers.com"
  aws_account    = "dev"
  aws_region     = "us-east-1"
  aws_account_id = "166273659435"
}