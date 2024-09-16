FROM --platform=linux/amd64 apache/airflow:slim-2.9.1-python3.12 AS base

USER root
ARG AIRFLOW_USER_HOME=/opt/airflow


ENV PYTHONPATH=${AIRFLOW_USER_HOME}
ENV AIRFLOW__CORE__LOAD_EXAMPLES='true'
# in a production environment, always fix the package version number
FROM base AS deps
USER airflow

RUN pip install apache-airflow-providers-microsoft-mssql apache-airflow-providers-amazon --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.1/constraints-3.12.txt"


FROM deps

ENV AIRFLOW__CORE__LOAD_EXAMPLES=True

VOLUME /opt/airflow/dags
ENTRYPOINT [ "airflow" ]
CMD ["standalone"]

