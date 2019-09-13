from typing import Generic, TypeVar, Optional, List, Any, Type
from typing_extensions import Literal

from pydantic import validator
from pydantic.generics import GenericModel

from pydantic_jsonapi.errors import Error
from pydantic_jsonapi.relationships import RelationshipsType
from pydantic_jsonapi.links import LinksType


TypeT = TypeVar('TypeT')
AttributesT = TypeVar('AttributesT')
class ResponseDataModel(GenericModel, Generic[TypeT, AttributesT]):
    id: str
    type: TypeT
    attributes: AttributesT
    relationships: Optional[RelationshipsType]


DataT = TypeVar('DataT')
class ResponseModel(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    included: Optional[dict]
    meta: Optional[dict]
    links: Optional[LinksType]
    errors: Optional[List[Error]]


def JsonApiResponse(type_string: str, attributes_model: Any) -> Type[ResponseModel]:
    return ResponseModel[
        ResponseDataModel[
            Literal[type_string],
            attributes_model,
        ],
    ]
