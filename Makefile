test:
	pytest ./src/tests

deploy:
	@echo "Deploying to AWS to dev"
	@echo "Making sure node node_modules are installed"
	npm i
	@echo "Running Serverless deploy"
	sls deploy --stage dev
	@echo "Deployment complete"

e2e:
	@echo "Running e2e tests"
	cd ./src/tests/e2e && npm i && npx cypress run -s cypress/e2e/e2e.cy.js && cd -
	@echo "e2e tests complete"
