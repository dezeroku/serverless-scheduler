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
import difflib

from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
from PIL import ImageColor

from bs4 import BeautifulSoup

DEVELOPMENT = False

def screenshot_url(url, filename):
    if not check_for_variable_existence(['SCREENSHOT_API']):
        sys.exit(1)

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
    result = True
    for var in variables:
        if os.environ.get(var) is None:
            logger.error('NOT SPECIFIED {}'.format(var))
            result = False
    return result

def started_mail(url):
    global DEVELOPMENT
    print("STARTED")
    # Create mail object
    attachments = []

    subject="Started monitoring {0}".format(url)
    content="""Hi user!<br> We started monitoring {0} for you.
<br>
It will be checked every {1} seconds. We will let you know if something changes.
<br>
MAY THE FORCE BE WITH YOU
<br>
We are changing for the better :)""".format(url, os.environ.get("SLEEP_TIME"))

    recipients = os.environ.get('MAIL_RECIPIENT').split() if not DEVELOPMENT else "mail_recipients"
    mail = {
        "data" : {
            "url" : url,
            "attachments" : attachments
        },
        "recipients" : recipients,
        "subject" : subject,
        "html_content" : content
        }

    if not DEVELOPMENT:
        if not check_for_variable_existence(['MAIL_RECIPIENT', 'SENDER_API']):
            sys.exit(1)

        r = requests.post("{0}/v1/mail".format(os.environ.get('SENDER_API')),
                         json=mail)
        if r.status_code == 200:
            print("Successfully sent.")
        else:
            print("Incorrect status code: {0}".format(r.status_code))
            print(r.json())
            sys.exit(1)
    else:
        print("started mail sent")
        print(mail)

def changes_mail(url, diff=""):
    global DEVELOPMENT
    print("CHANGED")

    # Create mail object.
    attachments = []
    if os.environ.get('MAKE_SCREENSHOTS') == '1':
        def attach_png(file_path):
            with open(file_path, 'rb') as f:
                    data = f.read()
                    f.close()
            encoded = base64.b64encode(data).decode()
            return {
                'filename' : file_path,
                'filetype' : 'image/png',
                'content' : encoded
            }

        mark_diff_images("old_state.png", "new_state.png", "diff.png")
        attachments = [attach_png('diff.png'), attach_png('real_diff.png')]

    subject = "Changes on {0}".format(url)
    content = """Changes were detected on the <a href="{0}">page you ordered to monitor</a>.
<br>
{1}
<br>
MAY THE FORCE BE WITH YOU""".format(url, diff)

    recipients = os.environ.get('MAIL_RECIPIENT').split() if not DEVELOPMENT else "mail_recipients"
    mail = {
        "data" : {
            "url" : url,
            "attachments" : attachments
        },
        "recipients" : recipients,
        "subject" : subject,
        "html_content" : content
        }

    if not DEVELOPMENT:
        if not check_for_variable_existence(['MAIL_RECIPIENT', 'SENDER_API']):
            sys.exit(1)

        r = requests.post("{0}/v1/mail".format(os.environ.get('SENDER_API')),
                         json=mail)
        if r.status_code == 200:
            print("Successfully sent.")
        else:
            print("Incorrect status code: {0}".format(r.status_code))
            print(r.json())
            sys.exit(1)
    else:
        print("change mail sent")
        print(mail)

def main():
    logger = logging.getLogger('main')
    if not check_for_variable_existence(['URL_TO_CHECK', 'SLEEP_TIME']):
        sys.exit(1)

    global DEVELOPMENT
    if os.environ.get("DEVELOPMENT") == "true":
        DEVELOPMENT = True

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
            first = BeautifulSoup(text, 'html.parser')
            logger.info("Initialized.")
        else:
            # Main checking loop.
            if temp.text == text:
                logger.info("Nothing changed on website.")
            else:
                print("CHANGES START")
                second = BeautifulSoup(temp.text, 'html.parser')
                differ = difflib.HtmlDiff()
                #diff = differ.make_table(first.prettify().split("\n"),
                #                         second.prettify().split("\n"), '', '',
                #                         True, 2)
                diff = ""

                logger.info("Changes detected.")
                if make_screenshots:
                    screenshot_url(url, "new_state.png")
                changes_mail(url, diff)
                if make_screenshots:
                    os.rename("new_state.png", "old_state.png")
                text = temp.text
                first = BeautifulSoup(text, 'html.parser')
                print("CHANGES DONE")
        time.sleep(int(os.environ.get("SLEEP_TIME")))

# if MAKE_SCREENSHOTS == 1 then SCREENSHOT_API has to be provided and correct
main()
