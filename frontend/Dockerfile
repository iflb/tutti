FROM node:lts-alpine3.12

ARG FRONTEND_HOME
WORKDIR $FRONTEND_HOME

RUN apk add git

COPY package.json* ./
COPY init.sh ./init.sh
RUN npm install

RUN chmod +x ./init.sh

ENTRYPOINT ["./init.sh"]
