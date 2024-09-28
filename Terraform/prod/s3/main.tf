module "s3" {
  source = "../../modules/s3"

  bucket_name    = "app.ironwatchers.com"
  aws_region     = "us-east-1"
  aws_account_id = "382905285032"
}
