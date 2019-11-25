# Manager

API utility that's responsible for contact with outside worlds.
It authorizes users by sending them mails with access link.
Its role is also to manage all the checkers that are currently running.

* APP_URL - basically a URL/hostname that this API is available under. It's used to properly address magic links.
* JWT_KEY - secret key used to sign JWT tokens.
* SENDER_API - should contain URL to an API that's responsible for sending stuff (sender)
* DATABASE_TYPE - defaults to postgres if not provided
* DATABASE_URL - gorm formatted url that contains information necessary to connect to DB

* DEVELOP_MODE - if set in environment, mail is not send and its content is displayed on the screen. Also dummy data is inserted into db.
