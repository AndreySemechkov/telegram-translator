module "custom_api_gateway" {
  source = "../../modules/custom_api_gateway"

  certificate_name    = "dev-app.ironwatchers.com"
  api_gateway_dns     = "dev-api.ironwatchers.com"
  aws_region          = "us-east-1"
}