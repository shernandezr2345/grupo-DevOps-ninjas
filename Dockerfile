# check=skip=SecretsUsedInArgOrEnv
FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Instalar New Relic
RUN pip install newrelic

# Configuración básica por variables de entorno
ENV NEW_RELIC_APP_NAME="entrega4"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG_LEVEL=info
ENV NEW_RELIC_LICENSE_KEY=2f3812560150e56e8531aecdab6f6a11FFFFNRAL
# IMPORTANTE: arrancar con newrelic-admin
CMD ["newrelic-admin", "run-program", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
