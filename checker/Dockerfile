FROM python:3.7

WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV SLEEP_TIME=600
#ENV URL_TO_CHECK=url \
#    MAIL_RECIPIENT=recipient \
#    MAIL_SENDER=sender \
#    SENDGRID_API_KEY=key

COPY . .

ENTRYPOINT ["python3", "monitor.py"]
