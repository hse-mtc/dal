### Step 1.
## Build front-end app.

# Latest Node image
FROM node:16-alpine AS builder

# Set working directory
WORKDIR /front-end

# Copy package[-lock].json
COPY front-end/package*.json ./

# Install python and stuff (for some reason, on ARM, node docker image does not have python)
RUN apk add --no-cache g++ gcc libgcc libstdc++ linux-headers make python3

# Install packages
RUN npm install --loglevel=error

# Copy everything else
ADD front-end .

# Reference build arguments
ARG VUE_APP_BACK_END_HOST
ARG VUE_APP_BACK_END_PORT

# Build front-end in directory `/front-end/dist`
RUN npm run build:production --loglevel=error

### Step 2.
## Serve build.

# Latest Nginx image
FROM nginx:stable-alpine

# Install bash for tools
RUN apk add --no-cache bash

# Copy tools
COPY tools tools

# Copy built front-end app
COPY --from=builder /front-end/dist /usr/share/nginx/html

# Expose port
EXPOSE 80
