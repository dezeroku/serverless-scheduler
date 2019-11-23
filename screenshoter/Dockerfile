FROM python:3.7

# Install chromium (version 78) and matching chromedriver.
ARG CHROMIUM_REVISION=693954
WORKDIR /root
RUN wget -O chrome-linux.zip https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/$CHROMIUM_REVISION/chrome-linux.zip
RUN pwd && ls && unzip chrome-linux.zip && mv chrome-linux/* /usr/bin

RUN wget -O chromedriver.zip http://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_linux64.zip
RUN unzip chromedriver.zip
RUN mv chromedriver /usr/bin/chromedriver && \
    chown root:root /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

RUN apt-get update && \
    apt-get install -y curl \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libxcomposite-dev \
    libxcursor-dev \
    libxtst-dev \
    libnss3-dev \
    libcups2 \
    libxrandr-dev \
    libasound-dev \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
