from decimal import Decimal

from items import utils


def test_replace_decimals():
    before = [
        {
            "owner": "s",
            "sleepTime": Decimal("60"),
            "id": Decimal("1"),
            "makeScreenshots": True,
            "url": "http://wp.pl",
        }
    ]
    after = [
        {
            "owner": "s",
            "sleepTime": 60,
            "id": 1,
            "makeScreenshots": True,
            "url": "http://wp.pl",
        }
    ]

    assert after == utils.replace_decimals(before)
