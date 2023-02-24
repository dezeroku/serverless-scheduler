from typing import Union

from pydantic import BaseModel, EmailStr, Extra


class BaseJob(BaseModel):
    """
    This class defines the minimum job definition that can be uniquely identified.
    It should only be used as a super class for more concrete job definitions.
    """

    user_email: EmailStr
    job_id: Union[int, None]  # pylint: disable=invalid-name

    class Config:
        extra = Extra.forbid
