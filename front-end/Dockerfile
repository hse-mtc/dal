FROM node:lts-alpine

ARG VUE_APP_LOCAL_DEPLOYMENT
ENV VUE_APP_LOCAL_DEPLOYMENT $VUE_APP_LOCAL_DEPLOYMENT

# install simple http server for serving static content
RUN npm install -g express

# make the 'app' folder the current working directory
WORKDIR /code

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory
COPY . .

# build app for production with minification
RUN npm run build:prod