#!/bin/bash

rm -rf ./.pid
envsubst '$$REDIS_ADDRESS' < ${BACKEND_HOME}/config_server.ini.template > ${BACKEND_HOME}/config_server.ini
python -m ducts server start
/bin/bash
