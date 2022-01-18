
build:
	docker build . -t dabbleofdevops/cellxgene-gateway:0.3.8
	docker build . -t dabbleofdevops/cellxgene-gateway:0.3.8-5
	docker build . -t dabbleofdevops/cellxgene-gateway:latest

up:
	 docker run -it -p 5005:5005 \
	 	-e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
		-e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
		-e CELLXGENE_BUCKET="cellxgene-gateway-example-set" \
		dabbleofdevops/cellxgene-gateway:0.3.8

dev:
	$(MAKE) build
	$(MAKE) up

push:
	$(MAKE) build
	docker push dabbleofdevops/cellxgene-gateway:0.3.8
	docker push dabbleofdevops/cellxgene-gateway:0.3.8-5
	docker push dabbleofdevops/cellxgene-gateway:latest