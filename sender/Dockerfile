FROM alpine:3.7

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

USER nginx
ENV PYTHONUNBUFFERED=1

COPY --chown=nginx:nginx . /usr/src/app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

CMD ["./start.sh"]
#CMD ["python3", "-m", "swagger_server"]
