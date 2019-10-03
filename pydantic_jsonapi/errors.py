from typing import Optional, List

from pydantic import BaseModel


class ErrorSource(BaseModel):
    pointer: Optional[str]
    parameter: Optional[str]


class Error(BaseModel):
    """
    currently incomplete representation of:
    https://jsonapi.org/format/#error-objects
    """
    status: int
    source: Optional[ErrorSource]


class ErrorResponse(BaseModel):
    errors: List[Error]
