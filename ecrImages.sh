#!/usr/bin/env bash
set -o errexit

AWS_REGION="${Region:=us-west-2}"
AWS_ACCOUNT="${AWSAcct:=880757707621}"

docker build -t ${AWS_ACCOUNT}.dkr.ecr.us-east-1.amazonaws.com/fastapigraphqlstarter -f Dockerfile .

aws ecr get-login-password --region ${AWS_REGION} \
	| docker login --username AWS --password-stdin \
	${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com && \
	docker push \
	${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/fastapigraphqlstarter:latest

