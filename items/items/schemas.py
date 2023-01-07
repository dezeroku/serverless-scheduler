from marshmallow import Schema, ValidationError, fields, post_load

from items.models import MonitorJob, UserData


def validate_sleep_time(value):
    if value < 1:
        raise ValidationError("sleepTime must be a positive number")


class MonitorJobSchema(Schema):
    id = fields.Int(required=True)
    make_screenshots = fields.Bool(
        data_key="makeScreenshots",
        dump_default=False,
    )
    sleep_time = fields.Int(
        data_key="sleepTime",
        required=True,
        validate=validate_sleep_time,
    )
    url = fields.URL(required=True)

    @post_load
    def create_model(self, data, **kwargs):
        # pylint: disable=unused-argument
        return MonitorJob(**data)


class UserDataSchema(Schema):
    id = fields.Str(required=True)
    monitors = fields.List(
        fields.Nested(MonitorJobSchema),
        dump_default=[],
        load_default=[],
    )

    @post_load
    def create_model(self, data, **kwargs):
        # pylint: disable=unused-argument
        return UserData(**data)
