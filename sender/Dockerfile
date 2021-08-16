FROM alpine:3.7 as base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Create user to run stuff.
RUN addgroup -S nginx && \
    adduser -S nginx -G nginx && \
    chown nginx:nginx /usr/src/app

RUN apk add uwsgi uwsgi-python3 nginx --no-cache

# Redirect nginx logs to STDOUT/ERR.
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

FROM base as test-base
COPY requirements_test.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements_test.txt

FROM base as build
COPY --chown=nginx:nginx . /usr/src/app

FROM test-base as test
COPY --from=build /usr/src/* ./
RUN python3 -m pytest

FROM build as production
USER nginx
ENV PYTHONUNBUFFERED=1
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

CMD ["./start.sh"]
