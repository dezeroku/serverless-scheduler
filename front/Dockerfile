FROM node:16.5.0-alpine as base
WORKDIR /app
COPY ./package.json ./package-lock.json ./
RUN npm install
COPY . ./

FROM base as test
ENV CI=true
RUN npm test

FROM base as build
RUN npm run build

FROM nginx:1.21-alpine as production
RUN apk add --no-cache bash
COPY --from=build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

WORKDIR /usr/share/nginx/html
COPY ./env.sh ./.env ./

EXPOSE 80

CMD ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]
