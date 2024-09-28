# Module Overview

This project utilizes several modules to provision and manage infrastructure resources. Each module is responsible for provisioning a specific set of resources.

## Module 1: ACM

The ACM module provisions an AWS Certificate Manager (ACM) certificate and sets up DNS validation using Route 53.

### Resources Created

- ACM Certificate: The module creates an ACM certificate for the specified domain name and subject alternative names.

- Route 53 Record: The module creates a Route 53 record for DNS validation of the ACM certificate.

## Module 2: S3

The S3 module provisions an S3 bucket for storing static assets and hosting the application's website.

### Resources Created

- S3 Bucket: The module creates an S3 bucket with the specified bucket name.

- S3 Bucket Policy: The module applies a bucket policy to allow public read access to the bucket.

## Module 3: CloudFront

The CloudFront module provisions a CloudFront distribution for content delivery and caching.

### Resources Created

- CloudFront Distribution: The module creates a CloudFront distribution with the specified domain name.

- Route 53 Record: The module creates a Route 53 record to associate the CloudFront distribution with the domain name.

By utilizing these modules, you can easily provision and manage the required infrastructure resources.

Tags: #module #overview #acm #s3 #cloudfront #terraform #aws
