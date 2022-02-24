SHELL := /bin/bash

DOCKER="dabbleofdevops/terraform:terraform-0.14"
VERSION?=0.0.01
SHA?=0.0.1
ECR_IMAGE="709825985650.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy"
DOCKERHUB_IMAGE="dabbleofdevops/k8s-shinyproxy"

# 018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy

-include $(shell curl -sSL -o .build-harness "https://git.io/build-harness"; echo .build-harness)

helm/dep:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add bioanalyze https://dabble-of-devops-bioanalyze.github.io/helm-charts/
	helm repo update

helm/build:
	$(MAKE) helm/dep
	PWD=$(shell pwd)

	cd charts/shinyproxy
	helm dep update
	helm dep build

	cd ../../charts/single-cell-cloud-lab
	helm dep update
	helm dep build

make-dirs:
	mkdir -p .aws

docker/build:
	echo "build"
	docker build -t k8s-shinyproxy images/shinyproxy
	docker tag k8s-shinyproxy:latest $(ECR_IMAGE):latest
	docker tag k8s-shinyproxy:latest $(ECR_IMAGE):$(VERSION)
	docker tag k8s-shinyproxy:latest $(ECR_IMAGE):$(SHA)
	docker tag k8s-shinyproxy:latest $(DOCKERHUB_IMAGE):latest
	docker tag k8s-shinyproxy:latest $(DOCKERHUB_IMAGE):$(VERSION)
	docker tag k8s-shinyproxy:latest $(DOCKERHUB_IMAGE):$(SHA)

docker/push:
	# push to dockerhub
	docker push $(DOCKERHUB_IMAGE):latest
	docker push $(DOCKERHUB_IMAGE):$(VERSION)
	docker push $(DOCKERHUB_IMAGE):$(SHA)
	# aws ecr
	# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 018835827632.dkr.ecr.us-east-1.amazonaws.com
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com
	docker push $(ECR_IMAGE):latest
	docker push $(ECR_IMAGE):$(VERSION)
	docker push $(ECR_IMAGE):$(SHA)

helm/readme:
	cd charts/shinyproxy && \
		readme-generator \
			--values values.yaml \
			--readme README.md \
			-m values.schema.json

	cd charts/single-cell-cloud-lab && \
		readme-generator \
			--values values.yaml \
			--readme README.md \
			-m values.schema.json

eks/shell:
	$(MAKE) make-dirs
	docker run --rm -it \
		--env-file "./.env" \
		-v $(shell pwd)/.aws:/root/.aws \
		-v $(shell pwd):/root/project \
		-v $(shell pwd)/../../terraform-recipes:/root/terraform-recipes \
		-w /root/project/helm_charts \
		$(DOCKER) bash

# Terraform stuff

download-readme:
	wget https://raw.githubusercontent.com/dabble-of-devops-bioanalyze/biohub-info/master/docs/README.md.gotmpl -O ./README.md.gotmpl

shinyproxy/custom-init:
	cd charts/shinyproxy && \
		docker run -it -v "$(shell pwd):/tmp/terraform-module" \
			-e README_TEMPLATE_FILE=/tmp/terraform-module/README.md.gotmpl \
			-w /tmp/terraform-module \
			cloudposse/build-harness:slim-latest init

# generate the readme

shinyproxy/custom-readme:
	$(MAKE) download-readme
	$(MAKE) shinyproxy/custom-init
	cd charts/shinyproxy && \
		docker run -it -v "$(shell pwd):/tmp/terraform-module" \
			-e README_TEMPLATE_FILE=/tmp/terraform-module/README.md.gotmpl \
			-w /tmp/terraform-module \
			cloudposse/build-harness:slim-latest readme