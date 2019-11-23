"""Screenshoter (Chrome)
Screenshot provided URL with Chrome.
d0ku 2019"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def screenshot_url(url, filename):
    """Take a screenshot of provided url and save it under provided filename."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    # Added to use disk instead of memory (docker may have limitations)
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)

    # Just some big value.
    driver.set_window_size(1920, 2160)

    screenshot = driver.save_screenshot(filename)
    driver.quit()
