FROM node:lts-alpine3.12

ARG FRONTEND_HOME
WORKDIR $FRONTEND_HOME

#RUN npm install -g npm
#COPY package.json* node_modules* ./
COPY package.json* ./
RUN npm install

CMD ["npm","run","build"]
#CMD ["/bin/ash"]
