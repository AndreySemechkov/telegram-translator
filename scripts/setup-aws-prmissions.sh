#!/bin/bash

USER=$1
ACCOUNT=$2

aws iam create-role --role-name LambdaCFRole --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'

aws iam detach-user-policy --user-name "$USER" --policy-arn "arn:aws:iam::"$ACCOUNT":policy/TgwatcherAppPolicy"
aws iam delete-policy --policy-arn "arn:aws:iam::"$ACCOUNT":policy/TgwatcherAppPolicy"

aws iam create-policy --policy-name TgwatcherAppPolicy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "cloudformation:DescribeStacks",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "lambda:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "lambda:GetFunction",
            "Resource": "arn:aws:lambda:us-east-1:'$ACCOUNT':function:*"
        },
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::'$ACCOUNT':role/LambdaCFRole"
        },
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "cloudformation:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "cloudformation:DescribeStackResource",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "cloudformation:ValidateTemplate",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:TagResource",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "apigateway:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "events:*",
            "Resource": "*"
        }
    ]
}'

aws iam attach-user-policy --user-name "$USER" --policy-arn "arn:aws:iam::"$ACCOUNT":policy/TgwatcherAppPolicy"

