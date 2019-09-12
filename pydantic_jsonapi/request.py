from typing import Generic, TypeVar, Optional

from pydantic.generics import GenericModel


AttributesT = TypeVar('AttributesT')
class RequestData(GenericModel, Generic[AttributesT]):
    type: str
    attributes: AttributesT


DataT = TypeVar('DataT')
class Request(GenericModel, Generic[DataT]):
    data: DataT
