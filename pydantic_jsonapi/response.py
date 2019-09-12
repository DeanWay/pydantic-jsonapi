from typing import Generic, TypeVar, Optional, List

from pydantic import validator
from pydantic.generics import GenericModel

from pydantic_jsonapi.errors import Error


AttributesT = TypeVar('AttributesT')
class ResponseData(GenericModel, Generic[AttributesT]):
    id: str
    type: str
    attributes: AttributesT
    relationships: Optional[dict]


DataT = TypeVar('DataT')
class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    included: Optional[dict]
    meta: Optional[dict]
    links: Optional[dict]
    errors: Optional[List[Error]]

    @validator('errors', always=True, whole=True)
    def check_consistency(cls, v, values):
        if v is not None and values['data'] is not None:
            raise ValueError('must not provide both data and errors')
        if v is None and values.get('data') is None:
            raise ValueError('must provide data or errors')
        return v
