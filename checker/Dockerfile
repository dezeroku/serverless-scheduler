FROM python:3.7 as base

WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

FROM base as test-base
COPY ./requirements_test.txt .
RUN pip3 install -r requirements_test.txt

FROM base as build
COPY ./*.py ./

FROM test-base as test
COPY --from=build /app/* ./
RUN python3 -m pytest

FROM base as production
ENV PYTHONUNBUFFERED=1
ENV SLEEP_TIME=600


ENTRYPOINT ["python3", "monitor.py"]
