FROM nginx

RUN apt-get update && apt-get install -y wget
ADD https://dl.eff.org/certbot-auto /usr/local/bin/certbot-auto
RUN chmod a+x /usr/local/bin/certbot-auto
RUN certbot-auto --os-packages-only -n
RUN certbot-auto --nginx -d ec2-mturk10-bak.r9n.net -m mturk10@pcl.cs.waseda.ac.jp --agree-tos -n
RUN certbot-auto renew
