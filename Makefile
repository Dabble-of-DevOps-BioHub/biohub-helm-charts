SHELL := /bin/bash

DOCKER="dabbleofdevops/terraform:terraform-0.14"

make-dirs:
	mkdir -p .aws

eks/shell:
	$(MAKE) make-dirs
	docker run --rm -it \
		--env-file "./.env" \
		-v $(shell pwd)/.aws:/root/.aws \
		-v $(shell pwd):/root/project \
		-v $(shell pwd)/../../terraform-recipes:/root/terraform-recipes \
		-w /root/project/helm_charts \
		$(DOCKER) bash