#!/bin/bash

# These are the prerequisite components to create remote state files for TF.
# We need to run these commands before we run 'terraform init' for new infra creation.
# Change params accordingly and execute from a local shell.
#------------------------------------------------------------------------------------------

aws_account="dev" 
profile="iron-dev"      # Choose the right profile under ~/.aws/credentials
key="s3"                # components to deploy; s3/acm/cloudfront, etc'
region="us-east-1"

# Run once per aws_account (dev/stage/prod)
AWS_PROFILE=$profile aws s3api create-bucket --bucket "terraform-state-ironwatchers-$aws_account"
AWS_PROFILE=$profile aws s3api put-public-access-block --bucket "terraform-state-ironwatchers-$aws_account" --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
AWS_PROFILE=$profile aws s3api put-bucket-versioning --bucket "terraform-state-ironwatchers-$aws_account" --versioning-configuration Status=Enabled
AWS_PROFILE=$profile aws s3api put-bucket-encryption --bucket "terraform-state-ironwatchers-$aws_account" --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'

# Run on init of new infra (s3/acm/cloudfront...)
AWS_PROFILE=$profile aws dynamodb create-table --table-name "terraform-state-ironwatchers-$aws_account-$key" --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --region $region