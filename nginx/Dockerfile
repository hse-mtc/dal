FROM nginx:stable-alpine

RUN apk add --no-cache bash
RUN mkdir -p /var/www/certbot

COPY nginx/prod.conf /etc/nginx/conf.d/default.conf
