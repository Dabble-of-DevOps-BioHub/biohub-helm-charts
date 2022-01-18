FROM continuumio/miniconda3

ARG CELLXGENE_GATEWAY_VERSION=0.3.8

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
	unzip awscliv2.zip && \
	./aws/install; \
	rm -rf awscliv2.zip

COPY environment.yml /tmp
COPY pbmc3k.h5ad /root/pbmc3k.h5ad

RUN conda env create  -f /tmp/environment.yml && \
	conda clean --all -y

ENV CONDA_PREFIX="/opt/conda/envs/cellxgene-gateway"
ENV CONDA_PROMPT_MODIFIER="(cellxgene-gateway)"
ENV CONDA_PYTHON_EXE="/opt/conda/bin/python"
ENV CONDA_DEFAULT_ENV="cellxgene-gateway"
ENV GATEWAY_PORT="5005"

ENV PATH="/opt/conda/envs/cellxgene-gateway/bin:${PATH}"
ENV CELLXGENE_LOCATION="/opt/conda/envs/cellxgene-gateway/bin/cellxgene"

COPY app /opt/app
WORKDIR /opt/app

CMD ["gunicorn", "gateway:app", "--bind", "0.0.0.0:5005"]
