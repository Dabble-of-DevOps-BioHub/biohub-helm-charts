SHELL := /bin/bash

DOCKER="dabbleofdevops/terraform:terraform-0.14"

VERSION?=0.0.01
SHA?=0.0.1
ECR_IMAGE="709825985650.dkr.ecr.us-east-1.amazonaws.com/dabble-of-devops/k8s-shinyproxy"
P_ECR_IMAGE="018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy"
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

	cd charts/shinyproxy && \
		helm dep update && \
		helm dep build

	cd charts/single-cell-cloud-lab && \
		helm dep update && \
		helm dep build

make-dirs:
	mkdir -p .aws

docker/build:
	echo "build"
	docker build -t k8s-shinyproxy images/shinyproxy

	docker tag k8s-shinyproxy:latest $(ECR_IMAGE):$(VERSION)
	docker tag k8s-shinyproxy:latest $(ECR_IMAGE):$(SHA)

	docker tag k8s-shinyproxy:latest $(P_ECR_IMAGE):$(VERSION)
	docker tag k8s-shinyproxy:latest $(P_ECR_IMAGE):$(SHA)

	docker tag k8s-shinyproxy:latest $(DOCKERHUB_IMAGE):latest
	docker tag k8s-shinyproxy:latest $(DOCKERHUB_IMAGE):$(VERSION)
	docker tag k8s-shinyproxy:latest $(DOCKERHUB_IMAGE):$(SHA)

docker/push:
	# push to dockerhub
	echo "PUshing dockerhub images"
	docker push -q $(DOCKERHUB_IMAGE):latest || echo 'Unable to push image'
	docker push -q $(DOCKERHUB_IMAGE):$(VERSION) || echo 'Unable to push image'
	docker push -q $(DOCKERHUB_IMAGE):$(SHA) || echo 'Unable to push image'

	# push to aws private ecr for scans
	echo "Pushing AWS ECR Images"
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 018835827632.dkr.ecr.us-east-1.amazonaws.com

	docker push -q $(P_ECR_IMAGE):$(SHA) || echo 'Unable to push image'
	docker push -q $(P_ECR_IMAGE):$(VERSION) || echo 'Unable to push image'

	# push to ecr
	echo "Pushing AWS ECR Marketplace Images"
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com

	docker push -q $(ECR_IMAGE):$(SHA) || echo 'Unable to push image'
	docker push -q $(ECR_IMAGE):$(VERSION) || echo 'Unable to push image'


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


ecr/describe:
	aws ecr describe-image-scan-findings \
		--registry-id 709825985650 \
		--repository-name k8s-single-cell-cloud-lab  \
		--image-id imageDigest=sha256:d606b5007f35c51b026e1ca7de713baf37b62c726fac8227173d8d1930cc6cf4