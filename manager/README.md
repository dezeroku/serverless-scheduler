# Manager

API utility that's responsible for contact with outside worlds.
It authorizes users by sending them mails with access link.
Its role is also to manage all the checkers that are currently running.

* APP_URL - basically a URL/hostname that this API is available under. It's used to properly address magic links.
* JWT_KEY - secret key used to sign JWT tokens.
* DATABASE_TYPE - defaults to postgres if not provided
* DATABASE_URL - gorm formatted url that contains information necessary to connect to DB
* CHECKER_IMAGE - URL to the docker image that should be run as a checker job
* CHECKER_NAMESPACE - k8s namespace in which checker job should be created

* SCREENSHOT_API_PORT - port exposed by the screenshot service
* SENDER_API_PORT - port exposed by the sender service
* COMPARATOR_API_PORT - port exposed by the comparator service

* SCREENSHOT_SERVICE - name of the screenshot service
* SENDER_SERVICE - name of the screenshot service
* COMPARATOR_SERVICE - name of the screenshot service

* DEVELOP_MODE - if set in environment, mail is not send and its content is displayed on the screen. Also dummy data is inserted into db.
