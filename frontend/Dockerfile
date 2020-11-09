FROM node:lts-alpine3.12

ARG FRONTEND_HOME
WORKDIR $FRONTEND_HOME

RUN apk update && \
    npm install -g npm && \
    npm install -g @vue/cli && \
    npm install

CMD ["npm","run","serve"]
