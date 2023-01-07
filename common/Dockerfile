FROM public.ecr.aws/lambda/python:3.8 as base

RUN yum update && \
    yum install -y zip

ENV PATH=$PATH:/root/.local/bin
RUN curl https://install.python-poetry.org | python3 - --version 1.3.0

WORKDIR /app/builder

COPY .packaging/temp /app/common
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

ARG COMPONENT_NAME
COPY $COMPONENT_NAME $COMPONENT_NAME

RUN poetry build -f wheel

RUN poetry run pip install --upgrade -t lambda-package dist/*.whl && \
    cd lambda-package && \
    zip -r /lambda.zip . -x '*.pyc' && \
    mv ../dist/*.whl /

FROM scratch as zip
COPY --from=base /lambda.zip .
COPY --from=base /*.whl .
