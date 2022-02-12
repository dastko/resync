FROM python:3.8 AS build
MAINTAINER Davor Stankovic

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN export PYTHONPATH="/app"
COPY requirements.txt ./

RUN echo "Installing dependencies ..."
RUN pip3 install --user --upgrade pip
RUN pip3 install --user --requirement requirements.txt

###

FROM python:3.8-slim

WORKDIR /app
RUN mkdir -p /var/log/supervisor
COPY scripts/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN apt-get update && apt-get -y install netcat && apt-get install -y supervisor && apt-get clean

COPY --from=build /root/.local /root/.local

RUN echo "Copy data ..."
COPY api /app/api
COPY domain /app/domain
COPY utils /app/utils
COPY envs /app/envs
COPY service /app/service
COPY scripts/ /app/scripts
COPY app.py /app
COPY local_run.py /app
COPY middleware.py /app
COPY config.py /app

RUN export PATH=$PATH:/root/.local/bin
RUN chmod +x /app/scripts/run.sh

CMD ["/usr/bin/supervisord"]
