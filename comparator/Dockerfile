FROM python:3.7 as base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install the lib dependencies
RUN apt-get update && \
    apt-get install -y python3-opencv

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

FROM base as test-base
COPY requirements_test.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements_test.txt

FROM base as build
COPY . /usr/src/app

FROM test-base as test
COPY --from=build /usr/src/* ./
RUN python3 -m pytest

FROM build as production
EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]