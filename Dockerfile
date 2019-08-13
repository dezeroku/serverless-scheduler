FROM python:3.7

WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

ENV URL_TO_CHECK=https://jpiatkowski.com
ENV SLEEP_TIME=600
ENV MAIL_RECIPIENT=darthtyranus666666@gmail.com
ENV MAIL_SENDER=fikumikunapatykuelobenc@gmail.com
ENV MAIL_PASSWORD=Ble#ble#ble#1#Hashlowanie
ENV MAIL_HOST=smtp.gmail.com
ENV MAIL_PORT=587

ENTRYPOINT ["python3", "monitor.py"]
