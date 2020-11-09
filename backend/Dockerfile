FROM python:3.9-buster

ARG BACKEND_HOME
WORKDIR $BACKEND_HOME

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y redis-server

ENTRYPOINT ["./init.sh"]
