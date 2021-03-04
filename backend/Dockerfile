FROM python:3.9-slim-buster

ARG BACKEND_HOME

WORKDIR ${BACKEND_HOME}

RUN apt-get update && \
    apt-get install -y gcc gettext-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config_server.ini.template ./config_server.ini.template
COPY init.sh ./init.sh
RUN chmod +x ./init.sh

ENTRYPOINT ["./init.sh"]
