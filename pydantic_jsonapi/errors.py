from typing import Optional, List

from pydantic import BaseModel
from pydantic_jsonapi.resource_links import ResourceLinks


class ErrorSource(BaseModel):
    pointer: Optional[str]
    parameter: Optional[str]


class Error(BaseModel):
    """https://jsonapi.org/format/#error-objects"""
    id: Optional[str]
    links: Optional[ResourceLinks]
    status: Optional[str]
    code: Optional[str]
    title: Optional[str]
    detail: Optional[str]
    source: Optional[ErrorSource]
    meta: Optional[dict]


class ErrorResponse(BaseModel):
    errors: List[Error]
