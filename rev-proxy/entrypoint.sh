#!/bin/ash
nginx
certbot --nginx -d ${DOMAIN_NAME} -m ${EMAIL} --agree-tos -n
certbot renew
nginx -s reload
/bin/ash
