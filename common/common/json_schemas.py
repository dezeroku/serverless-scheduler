all_schema = {"oneOf": [{"$ref": "item.json"}, {"$ref": "itemWithId.json"}]}

item_schema = {
    "$schema": "http://json-schema.org/schema#",
    "description": "Single monitoring job",
    "properties": {
        "make_screenshots": {"type": "boolean"},
        "sleep_time": {"type": "integer"},
        "url": {"type": "string"},
    },
    "required": ["url", "sleep_time", "make_screenshots"],
    "type": "object",
}

itemwithid_schema = {
    "$schema": "http://json-schema.org/schema#",
    "allOf": [
        {
            "$schema": "http://json-schema.org/schema#",
            "description": "Single monitoring job",
            "properties": {
                "make_screenshots": {"type": "boolean"},
                "sleep_time": {"type": "integer"},
                "url": {"type": "string"},
            },
            "required": ["url", "sleep_time", "make_screenshots"],
            "type": "object",
        },
        {
            "properties": {"id": {"type": "integer"}},
            "required": ["id"],
            "type": "object",
        },
    ],
    "type": "object",
}
