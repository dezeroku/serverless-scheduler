all_schema = {
    "oneOf": [
        {
            "$ref": "item.json"
        },
        {
            "$ref": "itemWithId.json"
        }
    ]
}

item_schema = {
    "$schema": "http://json-schema.org/schema#",
    "description": "Single monitoring job",
    "properties": {
        "makeScreenshots": {
            "type": "boolean"
        },
        "sleepTime": {
            "type": "integer"
        },
        "url": {
            "type": "string"
        }
    },
    "required": [
        "url",
        "sleepTime",
        "makeScreenshots"
    ],
    "type": "object"
}

itemwithid_schema = {
    "$schema": "http://json-schema.org/schema#",
    "allOf": [
        {
            "$schema": "http://json-schema.org/schema#",
            "description": "Single monitoring job",
            "properties": {
                "makeScreenshots": {
                    "type": "boolean"
                },
                "sleepTime": {
                    "type": "integer"
                },
                "url": {
                    "type": "string"
                }
            },
            "required": [
                "url",
                "sleepTime",
                "makeScreenshots"
            ],
            "type": "object"
        },
        {
            "properties": {
                "id": {
                    "type": "integer"
                }
            },
            "required": [
                "id"
            ],
            "type": "object"
        }
    ],
    "type": "object"
}

