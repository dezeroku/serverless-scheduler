"""Page Monitor
Periodically check for changes in HTML code of webpage and notify users if
detected.
d0ku 2019"""

import requests
import os
import sys
import logging
import time
import smtplib


def check_for_variable_existence(variables):
    logger = logging.getLogger('checker')
    for var in variables:
        if os.environ.get(var) is None:
            logger.error('NOT SPECIFIED {}'.format(var))
            return False
    return True


def changes_mail(url):
    logger = logging.getLogger('email')
    if not check_for_variable_existence(['MAIL_RECIPIENT', 'MAIL_SENDER',
                                        'MAIL_PASSWORD', 'MAIL_HOST',
                                         'MAIL_PORT']):
        return

    to = os.environ.get("MAIL_RECIPIENT")
    subject = "Changes detected on " + url
    message = """Changes were detected on the page you ordered to monitor.
MAY THE FORCE BE WITH YOU"""

    sender = os.environ.get("MAIL_SENDER")
    password = os.environ.get("MAIL_PASSWORD")

    host = os.environ.get("MAIL_HOST")
    try:
        port = int(os.environ.get("MAIL_PORT"))
    except ValueError:
        logger.error("Cannot convert MAIL_PORT to integer")
        return

    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(sender, password)

    body = '\r\n'.join(['To: %s' % to,
                        'From: %s' % sender, 'Subject: %s' % subject,
                        '', message])

    try:
        server.sendmail(sender, [to], body)
        logger.info("Email sent")
    except:
        logger.error("Could not send email")

    server.quit()


def main():
    logger = logging.getLogger('main')
    if not check_for_variable_existence(['URL_TO_CHECK', 'SLEEP_TIME']):
        sys.exit(1)

    try:
        int(os.environ.get("SLEEP_TIME"))
    except ValueError:
        logger.error("SLEEP_TIME HAS TO BE AN INTEGER (seconds count)")
        sys.exit(3)

    text = None
    while True:
        print("LOOP")
        temp = requests.get(os.environ.get("URL_TO_CHECK"))
        if text is None:
            # First time check.
            text = temp.text
            logger.info("Initialized.")
        else:
            # Main checking loop.
            if temp.text == text:
                logger.info("Nothing changed on website.")
            else:
                logger.info("Changes detected.")
                changes_mail(os.environ.get("URL_TO_CHECK"))
        time.sleep(int(os.environ.get("SLEEP_TIME")))


changes_mail(os.environ.get("URL_TO_CHECK"))
#main()
