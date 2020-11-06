FROM nginx

RUN apt-get update && apt-get install -y wget
ADD https://dl.eff.org/certbot-auto /usr/local/bin/certbot-auto
RUN chmod a+x /usr/local/bin/certbot-auto
RUN certbot-auto --os-packages-only -n
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
