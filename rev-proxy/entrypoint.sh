#!/bin/ash
certbot certonly --nginx -d ${DOMAIN_NAME} -m ${EMAIL} --agree-tos -n
certbot renew
nginx
/bin/ash
