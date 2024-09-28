### To support multiple environment we are going to use 3 tools:
- terraform: 
	- will create the resources
		- MongoDB Collection (we use 1 mongoDB Instance)
		- API Gateway domain and map it to the management account where the domain is registered.
		- Create the ACM Certificate
	- Secrets per env (store secrets in SSM) using KMS
- serverless-framework
	- will map api gateway to domain mapping created by terraform
	- will embed env vars the app layers could use for:
		- which DB Collection to use
		- which API Domain to use (so if 1 lambda needs to access another lambda, which domain to access).
		
- github actions - will run the deployment process with flags to indicate which envs to use, so when deploying to staging tell it to go to staging and so on. How:
	- it needs to know which bucket to deploy to
	- it needs to tell npm which env it works with
	- it needs to tell serverless framework which backend to deploy to

Here's a schematic drawing showing the flow

![[Supporting multiple envs in the app layer|700x400]]