
build:
	docker build . -t dabbleofdevops/cellxgene-gateway:0.3.8
	docker build . -t dabbleofdevops/cellxgene-gateway:0.3.8-5
	docker build . -t dabbleofdevops/cellxgene-gateway:latest


up:
	 docker run -it -p 5005:5005 \
	 	-e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
		-e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
		-e CELLXGENE_BUCKET="cellxgene-gateway-example-set" \
		-e ANNOTATION_DIR="/root/data" \
		-e SYNC_ENABLED="True" \
		-v ~/.aws:/root/.aws \
		-v $(shell pwd)/airflow/logs:/root/airflow/logs \
		-v $(shell pwd)/airflow/dags:/root/airflow/dags \
		-v $(shell pwd)/app:/opt/app \
		-v $(shell pwd)/data:/root/data \
		dabbleofdevops/cellxgene-gateway:0.3.8

launch:
	$(MAKE) build
	 docker run -it -p 5006:5005 \
		-e ANNOTATION_DIR="/root/data" \
		-e SYNC_ENABLED="True" \
		-v ~/.aws:/root/.aws \
		-v $(shell pwd)/airflow/logs:/root/airflow/logs \
		-v $(shell pwd)/app:/opt/app \
		-v $(shell pwd)/data:/root/data \
		dabbleofdevops/cellxgene-gateway:0.3.8 bash -c "cd /root/data; source activate cellxgene-gateway; cellxgene launch --host 0.0.0.0 --port 5005 s3://cellxgene-gateway-example-set/pbmc3k.h5ad"

dev:
	$(MAKE) build
	$(MAKE) up

compose/up:
	docker-compose build
	docker-compose up -d

compose/shell:
	docker-compose exec -it cellxgene bash

shell:
	$(MAKE) build
	 docker run -it \
	 	-e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
		-e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
		-e CELLXGENE_BUCKET="cellxgene-gateway-example-set" \
		-e ANNOTATION_DIR="/root/data" \
		-e SYNC_ENABLED="True" \
		-v ~/.aws:/root/.aws \
		-v $(shell pwd)/airflow/dags:/root/airflow/dags \
		-v $(shell pwd)/airflow/logs:/root/airflow/logs \
		-v $(shell pwd)/app:/opt/app \
		-v $(shell pwd)/data:/root/data \
		dabbleofdevops/cellxgene-gateway:0.3.8 bash

push:
	$(MAKE) build
	docker push dabbleofdevops/cellxgene-gateway:0.3.8
	docker push dabbleofdevops/cellxgene-gateway:0.3.8-5
	docker push dabbleofdevops/cellxgene-gateway:latest