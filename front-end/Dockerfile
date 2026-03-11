FROM node:16-alpine

RUN apk add --no-cache python3 make g++

WORKDIR /front-end

COPY front-end/package*.json ./
RUN npm install --loglevel=error

ADD front-end .

ARG VUE_APP_BACK_END_HOST
ARG VUE_APP_BACK_END_PORT

# Сборка в /front-end/dist
RUN npm run build:production --loglevel=error
