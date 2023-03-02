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
        "sleep_time": {
            "type": "integer"
        }
    },
    "required": [
        "sleep_time",
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
                "sleep_time": {
                    "type": "integer"
                }
            },
            "required": [
                "sleep_time",
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
