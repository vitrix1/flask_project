import pydantic
from typing import Type


class CreateAd(pydantic.BaseModel):
    header: str
    description: str
    owner: str


VALIDATION_CLASS = Type[CreateAd]
