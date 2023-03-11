all_schema = {
    "oneOf": [
        {
            "$ref": "job.json"
        },
        {
            "$ref": "jobWithId.json"
        }
    ]
}
job_schema = {
    "$schema": "http://json-schema.org/schema#",
    "description": "Single monitoring job",
    "properties": {
        "job_type": {
            "type": "string"
        },
        "make_screenshots": {
            "type": "boolean"
        },
        "sleep_time": {
            "type": "integer"
        },
        "url": {
            "type": "string"
        }
    },
    "required": [
        "url",
        "sleep_time",
        "make_screenshots",
        "job_type"
    ],
    "type": "object"
}
jobwithid_schema = {
    "$schema": "http://json-schema.org/schema#",
    "allOf": [
        {
            "$schema": "http://json-schema.org/schema#",
            "description": "Single monitoring job",
            "properties": {
                "job_type": {
                    "type": "string"
                },
                "make_screenshots": {
                    "type": "boolean"
                },
                "sleep_time": {
                    "type": "integer"
                },
                "url": {
                    "type": "string"
                }
            },
            "required": [
                "url",
                "sleep_time",
                "make_screenshots",
                "job_type"
            ],
            "type": "object"
        },
        {
            "properties": {
                "job_id": {
                    "type": "integer"
                },
                "user_email": {
                    "type": "string"
                },
                "user_id": {
                    "type": "string"
                }
            },
            "required": [
                "job_id",
                "user_email",
                "user_id"
            ],
            "type": "object"
        }
    ],
    "type": "object"
}
