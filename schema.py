import pydantic
from typing import Optional, Type, Union


class CreateAdvertisment(pydantic.BaseModel):
    title: str
    text: str
    author: str


class PatchAdvertisment(pydantic.BaseModel):
    title: Optional[str]
    text: Optional[str]
    author: Optional[str]


Validation = Union[Type[CreateAdvertisment], Type[PatchAdvertisment]]