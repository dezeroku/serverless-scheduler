FROM python:3.7

WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV SLEEP_TIME=600

COPY monitor.py .

ENTRYPOINT ["python3", "monitor.py"]
