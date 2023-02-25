from typing import Union

from pydantic import BaseModel, Extra


class BaseJob(BaseModel):
    """
    This class defines the minimum job definition that can be uniquely identified.
    It should be used as a super class for more concrete job definitions.
    """

    user_id: str
    job_id: Union[int, None]  # pylint: disable=invalid-name

    def get_unique_job_id(self) -> str:
        """
        Return unique identifier for the job
        """
        if self.job_id is None:
            raise ValueError("Can't get unique job id if job_id is None")
        return (self.user_id + "-" + str(self.job_id))[:127]

    class Config:
        extra = Extra.forbid
