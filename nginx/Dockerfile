FROM nginx:stable-alpine

RUN apk add --no-cache bash
RUN mkdir -p /var/www/certbot

RUN rm -f /etc/nginx/conf.d/default.conf

ARG NGINX_CONF=nginx/dev.conf
COPY ${NGINX_CONF} /etc/nginx/nginx.conf
