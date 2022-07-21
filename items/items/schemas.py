from marshmallow import (
    Schema,
    fields,
    post_load,
)

from items.models import (
    UserData,
    MonitorJob,
)


class MonitorJobSchema(Schema):
    id = fields.Int(required=True)
    make_screenshots = fields.Bool(
        data_key="makeScreenshots",
        dump_default=False,
    )
    sleep_time = fields.Int(
        data_key="sleepTime",
        required=True,
    )
    url = fields.URL(required=True)

    @post_load
    def create_model(self, data, **kwargs):
        return MonitorJob(**data)


class UserDataSchema(Schema):
    id = fields.Str(required=True)
    monitors = fields.List(
        fields.Nested(MonitorJobSchema),
        dump_default=[],
    )

    @post_load
    def create_model(self, data, **kwargs):
        return UserData(**data)
