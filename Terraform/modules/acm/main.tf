data "aws_route53_zone" "ironwatchers" {
  provider     = aws.mgmt_account
  name         = var.root_domain
  private_zone = false
}
##############

resource "aws_acm_certificate" "ironwatchers" {
  domain_name               = var.domain_name
  subject_alternative_names = var.subject_alternative_names
  validation_method         = "DNS"
}

resource "aws_route53_record" "ironwatchers" {
  provider = aws.mgmt_account

  for_each = {
    for dvo in aws_acm_certificate.ironwatchers.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = data.aws_route53_zone.ironwatchers.zone_id
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 300
  type            = each.value.type
  zone_id         = each.value.zone_id
}

resource "aws_acm_certificate_validation" "ironwatchers" {
  certificate_arn         = aws_acm_certificate.ironwatchers.arn
  validation_record_fqdns = [for record in aws_route53_record.ironwatchers : record.fqdn]
}
