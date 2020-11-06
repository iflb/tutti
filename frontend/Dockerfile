FROM node:lts-alpine3.12

WORKDIR /app

RUN apk update && \
    npm install -g npm && \
    npm install -g @vue/cli && \
    npm install

CMD ["npm","run","serve"]
