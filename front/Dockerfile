FROM node:12.9.1-alpine as react-build
WORKDIR /app
COPY ./package.json ./package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM nginx:1.17-alpine
RUN apk add --no-cache bash
COPY --from=react-build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

WORKDIR /usr/share/nginx/html
COPY ./env.sh ./.env ./

EXPOSE 80

CMD ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]
