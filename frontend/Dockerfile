FROM node:lts-alpine3.12

ARG FRONTEND_HOME
WORKDIR $FRONTEND_HOME

#RUN npm install -g npm
#COPY package.json* node_modules* ./
COPY package.json* ./
COPY init.sh ./init.sh
RUN npm install

RUN chmod +x ./init.sh

ENTRYPOINT ["./init.sh"]
#CMD ["npm","run","build"]
#CMD ["/bin/ash"]
