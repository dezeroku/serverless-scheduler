"""Page Monitor
Periodically check for changes in HTML code of webpage and notify users if
detected.
d0ku 2019"""

import requests
import os
import sys
import logging
import time

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def check_for_variable_existence(variables):
    logger = logging.getLogger('checker')
    for var in variables:
        if os.environ.get(var) is None:
            logger.error('NOT SPECIFIED {}'.format(var))
            return False
    return True


def started_mail(url):
    logger = logging.getLogger('email')
    if not check_for_variable_existence(['MAIL_RECIPIENT', 'MAIL_SENDER',
                                         'SENDGRID_API_KEY']):
        return

    message = Mail(
        from_email=os.environ.get('MAIL_SENDER'),
        to_emails=os.environ.get("MAIL_RECIPIENT"),
        subject="Started monitoring " + url,
        html_content="""Hi user!<br> We started monitoring {} for you.
        <br>
MAY THE FORCE BE WITH YOU""".format(url)
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logger.info(response.status_code)
        logger.info(response.body)
        logger.info(response.headers)
    except Exception as e:
        logger.error(e.message)


def changes_mail(url):
    logger = logging.getLogger('email')
    if not check_for_variable_existence(['MAIL_RECIPIENT', 'MAIL_SENDER',
                                         'SENDGRID_API_KEY']):
        return

    message = Mail(
        from_email=os.environ.get('MAIL_SENDER'),
        to_emails=os.environ.get("MAIL_RECIPIENT"),
        subject="Changes detected on " + url,
        html_content="""Changes were detected on the page you ordered to monitor.
        <br>
MAY THE FORCE BE WITH YOU"""
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logger.info(response.status_code)
        logger.info(response.body)
        logger.info(response.headers)
    except Exception as e:
        logger.error(e.message)


def main():
    logger = logging.getLogger('main')
    if not check_for_variable_existence(['URL_TO_CHECK', 'SLEEP_TIME']):
        sys.exit(1)

    started_mail(os.environ.get('URL_TO_CHECK'))
    try:
        int(os.environ.get("SLEEP_TIME"))
    except ValueError:
        logger.error("SLEEP_TIME HAS TO BE AN INTEGER (seconds count)")
        sys.exit(3)

    text = None
    while True:
        logger.debug("Loop")
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


main()
