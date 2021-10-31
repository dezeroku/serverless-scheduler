FROM node:17.0.1-alpine as base

# Installs latest Chromium (92) package.
RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

WORKDIR /app
USER node

FROM base as dev
# Development stage

FROM base as production-base
USER root
COPY ./package.json ./package-lock.json ./
RUN chown -R node:node /app

USER node
RUN npm install

COPY . ./
USER root
RUN chown -R node:node /app
USER node

FROM production-base as test
# TODO: To run tests in the future

FROM production-base as production
CMD ["node", "index.js"]
