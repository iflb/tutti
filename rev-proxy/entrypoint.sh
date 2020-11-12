#!/bin/ash
nginx
if [ ${ENABLE_SSL} -eq 1 ] ; then
    certbot --nginx -d ${DOMAIN_NAME} -m ${EMAIL} --agree-tos -n
    certbot renew
    nginx -s reload
fi
/bin/ash
