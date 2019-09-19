from typing import Optional, List

from pydantic import BaseModel


class ErrorSource(BaseModel):
    pointer: Optional[str]
    parameter: Optional[str]


class Error(BaseModel):
    status: int
    source: Optional[ErrorSource]


class ErrorResponse(BaseModel):
    errors: List[Error]
