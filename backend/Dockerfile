FROM python:3.9-slim-buster

ARG BACKEND_HOME
WORKDIR $BACKEND_HOME

COPY requirements.txt ./

RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["./init.sh"]
