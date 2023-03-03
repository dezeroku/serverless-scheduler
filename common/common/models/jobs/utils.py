from enum import Enum


def parse_dict_to_job_factory(job_type_enum: Enum, map_enum_to_class):
    def parse_dict_to_job(data: dict):
        if not (job_type := data.get("job_type")):
            raise ValueError("No job_type provided")

        try:
            job_type_value = job_type_enum(job_type)
        except ValueError as exc:
            raise ValueError("Incorrect job_type provided") from exc

        print(type(job_type_value))
        job_class = map_enum_to_class(job_type_value)
        return job_class(**data)

    return parse_dict_to_job
