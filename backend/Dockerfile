FROM python:3.9-slim-buster

ARG BACKEND_HOME

WORKDIR ${BACKEND_HOME}

COPY requirements.txt ./
COPY config_server.ini.template ./config_server.ini.template
COPY init.sh ./init.sh

RUN apt-get update && \
    apt-get install -y gcc redis-server gettext-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./init.sh

ENTRYPOINT ["./init.sh"]
