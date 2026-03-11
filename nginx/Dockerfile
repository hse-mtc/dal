FROM nginx:stable-alpine

RUN apk add --no-cache bash
RUN mkdir -p /var/www/certbot

RUN rm -f /etc/nginx/conf.d/default.conf

COPY nginx/prod.conf /etc/nginx/nginx.conf

EXPOSE 80 443
