#!/bin/bash
certbot-auto certonly --nginx -d ${DOMAIN_NAME} -m ${EMAIL} --agree-tos -n
certbot-auto renew
nginx
/bin/bash
