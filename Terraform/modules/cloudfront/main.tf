
data "aws_acm_certificate" "domain_cert" {
  domain = var.domain_name
}

data "aws_s3_bucket" "app" {
  bucket = var.domain_name
}

data "aws_route53_zone" "ironwatchers" {
  provider     = aws.mgmt_account
  name         = var.root_domain
  private_zone = false
}
##################

resource "aws_cloudfront_distribution" "s3_cloudfront" {
  origin {
    domain_name = data.aws_s3_bucket.app.website_endpoint
    origin_id   = "S3Origin"

    custom_origin_config {
      http_port                = 80
      https_port               = 443
      origin_keepalive_timeout = 5
      origin_protocol_policy   = "http-only"
      origin_read_timeout      = 30
      origin_ssl_protocols     = ["TLSv1.2"]
    }
  }

  enabled = true

  viewer_certificate {
    acm_certificate_arn = data.aws_acm_certificate.domain_cert.arn
    ssl_support_method  = "sni-only"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Origin"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  aliases = ["${var.domain_name}"]

  price_class = "PriceClass_100"

  # We can block arab countries later on
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

resource "aws_route53_record" "cloudfront" {
  provider        = aws.mgmt_account
  zone_id         = data.aws_route53_zone.ironwatchers.zone_id
  name            = var.domain_name
  allow_overwrite = true

  type = "A"
  alias {
    name                   = aws_cloudfront_distribution.s3_cloudfront.domain_name
    zone_id                = aws_cloudfront_distribution.s3_cloudfront.hosted_zone_id
    evaluate_target_health = false
  }
}