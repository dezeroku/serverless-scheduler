from typing import Union

from pydantic import BaseModel, EmailStr, Extra


class BaseJob(BaseModel):
    """
    This class defines the minimum job definition that can be uniquely identified.
    It should only be used as a super class for more concrete job definitions.
    """

    user_email: EmailStr
    job_id: Union[int, None]  # pylint: disable=invalid-name

    def get_unique_job_id(self) -> str:
        """
        Return unique identifier for the job
        """
        if self.job_id is None:
            raise ValueError("Can't get unique job id if job_id is None")
        return (self.user_email.replace("@", "_") + "-" + str(self.job_id))[:127]

    class Config:
        extra = Extra.forbid
