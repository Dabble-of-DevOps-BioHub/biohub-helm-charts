SHELL := /bin/bash

DOCKER="dabbleofdevops/terraform:terraform-0.14"
VERSION?=0.0.01
SHA?=0.0.1

-include $(shell curl -sSL -o .build-harness "https://git.io/build-harness"; echo .build-harness)

helm/dep:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add bioanalyze https://dabble-of-devops-bioanalyze.github.io/helm-charts/
	helm repo update

helm/build:
	$(MAKE) helm/dep
	PWD=$(shell pwd)

	helm dep update
	helm dep build

helm/readme:
	readme-generator \
		--values values.yaml \
		--readme README.md \
		-m values.schema.json

# Terraform stuff

download-readme:
	wget https://raw.githubusercontent.com/dabble-of-devops-bioanalyze/biohub-info/master/docs/README.md.gotmpl -O ./README.md.gotmpl

custom-init:
	docker run -it -v "$(shell pwd):/tmp/terraform-module" \
		-e README_TEMPLATE_FILE=/tmp/terraform-module/README.md.gotmpl \
		-w /tmp/terraform-module \
		cloudposse/build-harness:slim-latest init

# generate the readme

custom-readme:
	$(MAKE) download-readme
	$(MAKE) custom-init
	docker run -it -v "$(shell pwd):/tmp/terraform-module" \
		-e README_TEMPLATE_FILE=/tmp/terraform-module/README.md.gotmpl \
		-w /tmp/terraform-module \
		cloudposse/build-harness:slim-latest readme
	$(MAKE) helm/readme
	rm -rf ./README.md.gotmpl