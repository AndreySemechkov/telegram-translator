resource "aws_s3_bucket" "app_bucket" {
  bucket        = var.bucket_name
  force_destroy = true

  object_lock_enabled = false

  request_payer = "BucketOwner"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }

      bucket_key_enabled = true
    }
  }

  versioning {
    enabled    = false
    mfa_delete = false
  }

  website {
    index_document = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "app" {
  bucket = aws_s3_bucket.app_bucket.bucket

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "app" {
  depends_on = [aws_s3_bucket_public_access_block.app]

  bucket = aws_s3_bucket.app_bucket.bucket
  policy = jsonencode({
    "Statement" : [
      {
        "Action" : "s3:GetObject",
        "Effect" : "Allow",
        "Principal" : "*",
        "Resource" : "arn:aws:s3:::${var.bucket_name}/*",
        "Sid" : "PublicReadGetObject"
      },
      {
        "Action" : "s3:GetObject",
        "Condition" : {
          "StringLike" : {
            "aws:Referer" : [
              "http://${var.bucket_name}.s3-website.${var.aws_region}.amazonaws.com/*",
              "https://${var.bucket_name}.s3-website.${var.aws_region}.amazonaws.com/*"
            ]
          }
        },
        "Effect" : "Allow",
        "Principal" : {
          "AWS" : "*"
        },
        "Resource" : "arn:aws:s3:::${var.bucket_name}/*",
        "Sid" : "AddCORSRule"
      },
      {
        "Action" : [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        "Effect" : "Allow",
        "Principal" : {
          "AWS" : "arn:aws:iam::${var.aws_account_id}:role/OrganizationAccountAccessRole"
        },
        "Resource" : [
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ],
        "Sid" : "CrossAccountAccess"
      }
    ],
    "Version" : "2012-10-17"
  })
}
