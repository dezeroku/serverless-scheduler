"""Page Monitor
Periodically check for changes in HTML code of webpage and notify users if
detected (also send diffs).
d0ku 2019"""

import base64
import requests
import os
import sys
import logging
import time

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId )

from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
from PIL import ImageColor

def screenshot_url(url, filename):
    check_for_variable_existence(['SCREENSHOT_API'])
    r = requests.get("{0}/v1/screenshot".format(os.environ.get('SCREENSHOT_API')),
                     params={"url": url})
    if r.status_code == 200:
        decoded = base64.b64decode(r.json()['image'])
        with open(filename, 'wb') as f:
                f.write(decoded)
                f.close()
    else:
        print("Incorrect status code: {0}".format(r.status_code))
        sys.exit(1)

def mark_diff_images(first, second, output):
    im1 = Image.open(first)
    im2 = Image.open(second)

    im_diff = ImageChops.difference(im1, im2)
    diff = im_diff.getbbox()
    im2.crop(diff).save('real_diff.png')
    draw = ImageDraw.Draw(im2)
    diff_list = list(diff) if diff else []
    if diff_list:
        draw.rectangle(diff_list, outline=ImageColor.getrgb("red"), width=5)
    im2.convert('RGB').save(output)

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
        sys.exit(1)

    message = Mail(
        from_email=os.environ.get('MAIL_SENDER'),
        to_emails=os.environ.get("MAIL_RECIPIENT"),
        subject="Started monitoring " + url,
        html_content="""Hi user!<br> We started monitoring {0} for you.
<br>
It will be checked every {1} seconds. We will let you know if something changes.
<br>
MAY THE FORCE BE WITH YOU
<br>
We are changing for the better :)""".format(url, os.environ.get("SLEEP_TIME"))
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
    if os.environ.get('MAKE_SCREENSHOTS') == '1':
        mark_diff_images("old_state.png", "new_state.png", "diff.png")
    print("CHANGED")
    logger = logging.getLogger('email')
    if not check_for_variable_existence(['MAIL_RECIPIENT', 'MAIL_SENDER',
                                         'SENDGRID_API_KEY']):
        sys.exit(1)

    message = Mail(
        from_email=os.environ.get('MAIL_SENDER'),
        to_emails=os.environ.get("MAIL_RECIPIENT"),
        subject="Changes detected on " + url,
        html_content="""Changes were detected on the page you ordered to monitor.
<br>
MAY THE FORCE BE WITH YOU"""
    )

    def attach_png(file_path):
        with open(file_path, 'rb') as f:
                data = f.read()
                f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('image/png')
        attachment.file_name = FileName(file_path)
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId(file_path)
        return attachment

    if os.environ.get('MAKE_SCREENSHOTS') == '1':
        message.attachment = [attach_png('diff.png'), attach_png('real_diff.png')]

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

    try:
        int(os.environ.get("SLEEP_TIME"))
    except ValueError:
        logger.error("SLEEP_TIME HAS TO BE AN INTEGER (seconds count)")
        sys.exit(3)

    text = None
    url = os.environ.get('URL_TO_CHECK')
    make_screenshots = (os.environ.get('MAKE_SCREENSHOTS') == "1")
    if make_screenshots:
        screenshot_url(url, "old_state.png")
    if os.environ.get('STARTED_MAIL') == '1':
        started_mail(url)
    print("STARTED")
    while True:
        logger.debug("Loop")
        temp = requests.get(url)
        if text is None:
            # First time check.
            text = temp.text
            logger.info("Initialized.")
        else:
            # Main checking loop.
            if temp.text == text:
                logger.info("Nothing changed on website.")
            else:
                print("CHANGES START")
                logger.info("Changes detected.")
                if make_screenshots:
                    screenshot_url(url, "new_state.png")
                changes_mail(url)
                if make_screenshots:
                    os.rename("new_state.png", "old_state.png")
                text = temp.text
                print("CHANGES DONE")
        time.sleep(int(os.environ.get("SLEEP_TIME")))

# if MAKE_SCREENSHOTS == 1 then SCREENSHOT_API has to be provided and correct
main()
