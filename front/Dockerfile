FROM node:16.5.0 as base

WORKDIR /app

COPY ./tsconfig.json ./
COPY ./prepare-dist ./.env ./env.sh ./
COPY ./public ./public
COPY ./package.json ./package-lock.json ./
RUN npm ci

COPY ./src ./src

RUN npm run build && \
    npm run prepare-dist

FROM scratch as build-files
COPY --from=base /app/build .
