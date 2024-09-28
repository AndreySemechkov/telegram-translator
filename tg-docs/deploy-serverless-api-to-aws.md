# Deploy the Serverless API to AWS

1. Install Serverless

    ```bash
    npm install -g serverless
    ```

2. Install serverless plugins

    ```bash
    serverless plugin install -n serverless-python-requirements
    serverless plugin install -n serverless-functions-base-path
    serverless plugin install -n serverless-plugin-warmup
    ```

3. Validate python version on your env has the same as in serverless.yml runtime [possible deploy failure]

4. Install aws cli

5. AWS setup
    Create user or use existing one with permission to IAMFullAccess
    ```bash
    scripts/setup-aws-prmissions.sh <user> <aws-account>
    ```

6. Deploy the API

    ```bash
    serverless config credentials --provider aws --key <Your-Access-Key> --secret <Your-Secret-Key>
    sls deploy
    ```

    Troubleshooting:
    In case deployment fails due to missing permissions:
    ```bash
    run: sls remove
    copy the error with missing permission to chatgpt
    uncomment policy removal cmds in scripts/setup-aws-prmissions.sh line(19, 20)
    add the missing permission
    run: scripts/setup-aws-prmissions.sh <user> <aws-account>
    run: sls deploy
    ```

    Your results should look something like this:
    ```
    ✔ Service deployed to stack tgwatcher-dev (127s)
    endpoints:
        GET - https://epvb9ant11.execute-api.us-east-1.amazonaws.com/dev/message
        GET - https://epvb9ant11.execute-api.us-east-1.amazonaws.com/dev/message/{id}
    functions:
        scrap: tgwatcher-dev-scrap (18 MB)
        list: tgwatcher-dev-list (18 MB)
        get: tgwatcher-dev-get (18 MB)
        warmUpPlugin0: tgwatcher-dev-warmup-plugin-0 (1.2 kB)
    Stack Outputs:
        ScrapLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:532273734115:function:tgwatcher-dev-scrap:7
        WarmUpPlugin0LambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:532273734115:function:tgwatcher-dev-warmup-plugin-0:1
        GetLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:532273734115:function:tgwatcher-dev-get:7
        ListLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:532273734115:function:tgwatcher-dev-list:9
        ServiceEndpoint: https://epvb9ant11.execute-api.us-east-1.amazonaws.com/dev
        ServerlessDeploymentBucketName: tgwatcher-dev-serverlessdeploymentbucket-1vychipl10jvo
    ```

Tags: #Serverless #AWS #Deployment
