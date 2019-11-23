# Checker

Single core utility that keeps checking going on.

* STARTED_MAIL - if set to 1, sends 'welcome message', when monitoring starts
* SLEEP_TIME - in seconds, how long to wait between checks
* MAKE_SCREENSHOTS - if set to 1, takes screenshots of webpage and sends image diffs
* SCREENSHOT_API - if MAKE_SCREENSHOTS is enabled, it should contain URL to screenshoter container
* URL_TO_CHECK - URL of the page that should be monitored
* SENDGRID_API_KEY - API key to sendgrid (for sending emails)
* MAIL_SENDER - from whose account should be the mails send
* MAIL_RECIPIENT - who should be informed about changes (can be multiple emails, maybe comma separated?)
