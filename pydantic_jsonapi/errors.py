from typing import Optional

from pydantic import BaseModel


class ErrorSource(BaseModel):
    pointer: Optional[str]
    parameter: Optional[str]


class Error(BaseModel):
    status: int
    source: Optional[ErrorSource]
