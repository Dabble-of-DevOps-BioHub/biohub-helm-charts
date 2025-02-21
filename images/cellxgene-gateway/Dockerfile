#FROM continuumio/miniconda3
# FROM bitnami/python:3.6
FROM bitnami/airflow:2.2.3

ARG CELLXGENE_GATEWAY_VERSION=0.3.8
ENV CONDA_VERSION=4.10.3-7 \
    MAMBA_VERSION=0.17 \
    CONDA_ENV=cellxgene-gateway \
    NB_UID=1001 \
    SHELL=/bin/bash \
    LANG=C.UTF-8  \
    LC_ALL=C.UTF-8 \
    CONDA_DIR=/opt/bitnami/conda \
	DEBIAN_FRONTEND=noninteractive

ENV NB_PYTHON_PREFIX=${CONDA_DIR}/envs/${CONDA_ENV}
ENV PATH=${NB_PYTHON_PREFIX}/bin:${CONDA_DIR}/bin:${PATH}

WORKDIR /tmp

USER root
RUN apt-get update -y; apt-get install -y curl git wget unzip supervisor; rm -rf /var/lib/apt/lists/*

# install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
	unzip awscliv2.zip && \
	./aws/install && \
	rm -rf awscliv2.zip

USER 1001
RUN echo "Installing Miniforge..." \
    && URL="https://github.com/conda-forge/miniforge/releases/download/${CONDA_VERSION}/Miniforge3-${CONDA_VERSION}-Linux-x86_64.sh" \
    && wget --quiet ${URL} -O miniconda.sh \
    && /bin/bash miniconda.sh -u -b -p ${CONDA_DIR} \
    && rm miniconda.sh \
    && conda install -y -c conda-forge mamba=${MAMBA_VERSION} \
    && mamba clean -afy \
    && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
    && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete

COPY environment.yml /tmp
RUN mamba env create -f environment.yml && \
	mamba clean -yaf

# ENV PATH="/opt/conda/envs/cellxgene-gateway/bin:${PATH}"
# ENV CONDA_PREFIX="/opt/conda/envs/cellxgene-gateway"
# ENV CONDA_PROMPT_MODIFIER="(cellxgene-gateway)"
# ENV CONDA_PYTHON_EXE="/opt/conda/bin/python"
# ENV CONDA_DEFAULT_ENV="cellxgene-gateway"

# Cellxgene-gateway vars
ENV GATEWAY_PORT="5005"
ENV GATEWAY_ENABLE_ANNOTATIONS="True"
ENV CELLXGENE_LOCATION="${CONDA_DIR}/envs/cellxgene-gateway/bin/cellxgene"
ENV ANNOTATION_DIR="/opt/bitnami/airflow/data"
ENV HOME="/opt/bitnami"

RUN mkdir -p ${ANNOTATION_DIR}

# Airflow vars
ENV AIRFLOW__CORE__LOAD_EXAMPLES="False"
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION="False"

# Airflow
COPY install-airflow.sh /tmp/install-airflow.sh
# RUN chmod 777 *sh && bash /tmp/install-airflow.sh
# RUN  bash /tmp/install-airflow.sh

RUN airflow db init
COPY airflow/dags /opt/bitnami/airflow/dags

# Copy in some dummy data for testing
# RUN mkdir -p /root/data/

ENV APP_DIR="/opt/bitnami/projects/app"
RUN mkdir -p ${APP_DIR}
COPY app ${APP_DIR}
WORKDIR ${APP_DIR}

# DEV
# If running in dev and don't want to use supervisord or s3 sync just run directly
# CMD ["python", "gateway.py"]


# PROD
# Run the supervisord that spins up the airflow-scheduler and the log
CMD ["bash", "-c", "supervisord -c supervisord.conf; tail -f supervisord.log"]