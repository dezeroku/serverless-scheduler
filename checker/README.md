# Checker

Single core utility that keeps checking going on.

* STARTED_MAIL - if set to 1, sends 'welcome message', when monitoring starts
* SLEEP_TIME - in seconds, how long to wait between checks
* MAKE_SCREENSHOTS - if set to 1, takes screenshots of webpage and sends image diffs
* SCREENSHOT_API - if MAKE_SCREENSHOTS is enabled, it should contain URL to screenshoter container
* URL_TO_CHECK - URL of the page that should be monitored
* MAIL_RECIPIENT - who should be informed about changes (can be multiple emails, space separated)
* SENDER_API - should contain URL to an API that's responsible for sending stuff (sender)

TODO:
* using opencv to compare diff with images works a lot better than pure PIL, but is much more resource-hungry. Consider creating a new service or adding the funcionality of comparing images to one of the already existing to not impose too high limits on checkers.
