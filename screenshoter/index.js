const puppeteer = require('puppeteer-core');

var express = require('express');
var app = express();

var winston = require('winston'),
expressWinston = require('express-winston');

const apiVersion = "v1"

let browserInstance = null;
const getBrowserInstance = async function() {
    if (!browserInstance)
        browserInstance = await puppeteer.launch({
            args: ['--disable-dev-shm-usage'],
            executablePath: '/usr/bin/chromium-browser',
            defaultViewport: {
                width: 1920,
                height: 2160,
            },
        });
    return browserInstance;
}

getBrowserInstance();

const getURLScreenshot = async(url) => {
    const browser = await getBrowserInstance();
    const page = await browser.newPage();
    await page.goto(url);
    const to_return = await page.screenshot({ encoding: 'base64', type: 'png' });
    await page.close();

    return to_return;
}

app.use(expressWinston.logger({
    transports: [
        new winston.transports.Console()
    ],
    expressFormat: true
}));

app.get('/' + apiVersion + '/screenshot', function (req, res) {
    var url = req.query.url;
    new Promise((resolve, reject) => {
        getURLScreenshot(url)
            .then(data =>
                res.status(200).send({ image: data })
            )
            .catch(err =>
                {
                    console.log(err);
                    res.status(500).send({ message: err });
                }
            )
    })
})

app.get('/' + apiVersion + '/ready', function (req, res) {
    res.status(200).send("OK")
})

app.get('/' + apiVersion + '/live', function (req, res) {
    res.status(200).send("OK")
})

var server = app.listen(8080, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Screenshoter app listening at http://%s:%s", host, port)
})
