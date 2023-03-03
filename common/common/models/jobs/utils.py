from enum import Enum


def parse_dict_to_job_factory(job_type_enum: Enum, map_enum_to_class):
    def parse_dict_to_job(data: dict):
        job_type = data.pop("job_type")

        if not isinstance(job_type, job_type_enum):
            try:
                job_type_value = job_type_enum(job_type)
            except ValueError as exc:
                raise ValueError("Incorrect job_type provided") from exc
        else:
            job_type_value = job_type

        job_class = map_enum_to_class(job_type_value)
        return job_class(**data, job_type=job_type_value)

    return parse_dict_to_job
