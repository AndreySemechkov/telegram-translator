module "cloudfront" {
  source = "../../modules/cloudfront"

  domain_name    = "app.ironwatchers.com"
  aws_account    = "prod"
  aws_region     = "us-east-1"
  aws_account_id = "382905285032"
}
