#!/bin/bash
certbot-auto --nginx -d $DOMAIN_NAME -m $EMAIL --agree-tos -n
certbot-auto renew
/bin/bash
