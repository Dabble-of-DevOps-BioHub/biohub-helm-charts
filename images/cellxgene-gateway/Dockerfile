FROM continuumio/miniconda3

ARG CELLXGENE_GATEWAY_VERSION=0.3.8

WORKDIR /tmp
RUN apt-get update -y; apt-get install -y curl git wget unzip supervisor
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
	unzip awscliv2.zip && \
	./aws/install && \
	rm -rf awscliv2.zip

COPY environment.yml /tmp

RUN conda env create  -f /tmp/environment.yml && \
	conda clean --all -y

ENV PATH="/opt/conda/envs/cellxgene-gateway/bin:${PATH}"
ENV CONDA_PREFIX="/opt/conda/envs/cellxgene-gateway"
ENV CONDA_PROMPT_MODIFIER="(cellxgene-gateway)"
ENV CONDA_PYTHON_EXE="/opt/conda/bin/python"
ENV CONDA_DEFAULT_ENV="cellxgene-gateway"
ENV GATEWAY_PORT="5005"
ENV GATEWAY_ENABLE_ANNOTATIONS="True"
ENV CELLXGENE_LOCATION="/opt/conda/envs/cellxgene-gateway/bin/cellxgene"
ENV AIRFLOW__CORE__LOAD_EXAMPLES="False"
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION="False"

# Airflow
COPY install-airflow.sh /tmp/install-airflow.sh
RUN chmod 777 *sh && bash /tmp/install-airflow.sh

COPY dags /root/airflow/dags

# Copy in some dummy data for testing
RUN mkdir -p /root/data/
COPY data/pbmc3k.h5ad /root/data/pbmc3k.h5ad

COPY app /opt/app
WORKDIR /opt/app


# Run the supervisord that spins up the airflow-scheduler and the log
CMD ["bash", "-c", "supervisord -c supervisord.conf; tail -f supervisord.log"]
#CMD ["python", "gateway.py"]