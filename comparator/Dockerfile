FROM debian:stable-20210721
#FROM python:3.7-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y \
    uwsgi \
    uwsgi-plugin-python3 \
    nginx \
    python3-pip

# Redirect nginx logs to STDOUT/ERR.
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

RUN chown -R www-data:www-data /var/lib/nginx

# Skipped for now, as there are some problems with correct Python being used by uwsgi?
# So the openvcv gets built from sources at the moment
# Install the lib dependencies
#RUN apt-get update && \
#    apt-get install -y \
#python3-opencv

# Hardcode running builds on 4 threads (should match github action instances)
ARG MAKEFLAGS="-j4"

COPY requirements.txt /usr/src/app/

RUN python3 -m pip install --no-cache-dir -r requirements.txt

USER www-data

COPY --chown=www-data:www-data . /usr/src/app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

CMD ["./start.sh"]
