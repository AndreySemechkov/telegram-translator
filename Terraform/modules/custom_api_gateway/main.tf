
data "aws_acm_certificate" "domain_cert" {
  domain = var.certificate_name
}

data "aws_route53_zone" "ironwatchers" {
  provider     = aws.mgmt_account
  name         = var.root_domain
  private_zone = false
}
##################

resource "aws_apigatewayv2_domain_name" "gateway" {
  domain_name = var.api_gateway_dns

  domain_name_configuration {
    certificate_arn = data.aws_acm_certificate.domain_cert.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_route53_record" "gateway" {
  provider        = aws.mgmt_account
  zone_id         = data.aws_route53_zone.ironwatchers.zone_id
  name            = var.api_gateway_dns
  allow_overwrite = true

  type = "A"
  alias {
    name                   = aws_apigatewayv2_domain_name.gateway.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.gateway.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}