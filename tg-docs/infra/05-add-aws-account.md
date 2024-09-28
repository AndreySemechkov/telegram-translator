# Adding a New AWS Account

To add a new AWS account or environment to the project, follow these steps:

1. Open the `terraform.tfvars` file in the root directory of the project.

2. Add a new block of environment-specific variables for the new account. For example:

   ```hcl
   # New AWS Account
   aws_account_id = "123456789012"
   aws_region     = "us-west-2"
   ```

3. Save the changes to the `terraform.tfvars` file.

4. Create a new directory for the new account under the `tg-dev` or `tg-prod` directory, depending on the environment.

5. Copy the necessary Terraform files from an existing account directory and update any environment-specific configurations.

6. Initialize the Terraform environment for the new account by running `terraform init` in the new account directory.

7. Review the planned changes by running `terraform plan`.

8. If the planned changes look correct, apply the changes by running `terraform apply`.

By following these steps, you can add a new AWS account or environment to the project.

Tags: #aws #account #environment #terraform #configuration
