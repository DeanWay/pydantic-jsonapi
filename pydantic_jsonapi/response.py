from typing import Generic, TypeVar, Optional, List, Any, Type
from typing_extensions import Literal

from pydantic import validator
from pydantic.generics import GenericModel

from pydantic_jsonapi.errors import Error
from pydantic_jsonapi.filter import filter_none
from pydantic_jsonapi.relationships import RelationshipsType
from pydantic_jsonapi.links import LinksType


TypeT = TypeVar('TypeT')
AttributesT = TypeVar('AttributesT')
class ResponseDataModel(GenericModel, Generic[TypeT, AttributesT]):
    """
    """
    id: str
    type: TypeT
    attributes: AttributesT
    relationships: Optional[RelationshipsType]


DataT = TypeVar('DataT')
class ResponseModel(GenericModel, Generic[DataT]):
    """
    """
    data: DataT
    included: Optional[dict]
    meta: Optional[dict]
    links: Optional[LinksType]

    def dict(
        self,
        *,
        serlialize_none: bool = False,
        **kwargs
    ):
        response = super().dict(**kwargs)
        if serlialize_none:
            return response
        return filter_none(response)

def JsonApiResponse(
    type_string: str,
    attributes_model: Any,
    *,
    use_list: bool = False
) -> Type[ResponseModel]:
    response_data_model = ResponseDataModel[
        Literal[type_string],
        attributes_model,
    ]
    if use_list:
        response_data_model = List[response_data_model]
        response_data_model.__name__ = f'ListResponseData[{type_string}]'
        response_model = ResponseModel[response_data_model]
        response_model.__name__ = f'ListResponse[{type_string}]'
    else:
        response_data_model.__name__ = f'ResponseData[{type_string}]'
        response_model = ResponseModel[response_data_model]
        response_model.__name__ = f'Response[{type_string}]'
    return response_model
