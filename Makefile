SHELL := /bin/bash

DOCKER="dabbleofdevops/terraform:terraform-0.14"
VERSION?=0.0.01
SHA?=0.0.1

make-dirs:
	mkdir -p .aws

docker/build:
	echo "build"
	docker build -t k8s-shinyproxy images/shinyproxy
	docker tag k8s-shinyproxy:latest 018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy:latest
	docker tag k8s-shinyproxy:latest 018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy:$(VERSION)
	docker tag k8s-shinyproxy:latest 018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy:$(SHA)
	docker tag k8s-shinyproxy:latest dabbleofdevops/k8s-shinyproxy:latest
	docker tag k8s-shinyproxy:latest dabbleofdevops/k8s-shinyproxy:$(VERSION)
	docker tag k8s-shinyproxy:latest dabbleofdevops/k8s-shinyproxy:$(SHA)

docker/push:
	# push to dockerhub
	docker push dabbleofdevops/k8s-shinyproxy:latest
	docker push dabbleofdevops/k8s-shinyproxy:$(VERSION)
	docker push dabbleofdevops/k8s-shinyproxy:$(SHA)
	# aws ecr
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 018835827632.dkr.ecr.us-east-1.amazonaws.com
	docker push 018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy:latest
	docker push 018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy:$(VERSION)
	docker push 018835827632.dkr.ecr.us-east-1.amazonaws.com/k8s-shinyproxy:$(SHA)


eks/shell:
	$(MAKE) make-dirs
	docker run --rm -it \
		--env-file "./.env" \
		-v $(shell pwd)/.aws:/root/.aws \
		-v $(shell pwd):/root/project \
		-v $(shell pwd)/../../terraform-recipes:/root/terraform-recipes \
		-w /root/project/helm_charts \
		$(DOCKER) bash