FROM nginx

ARG DOMAIN_NAME

RUN echo $DOMAIN_NAME

RUN apt-get update && apt-get install -y wget
ADD https://dl.eff.org/certbot-auto /usr/local/bin/certbot-auto
RUN chmod a+x /usr/local/bin/certbot-auto
RUN certbot-auto --os-packages-only -n
RUN certbot-auto --nginx -d $DOMAIN_NAME -m $EMAIL --agree-tos -n
RUN certbot-auto renew
