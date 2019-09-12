from typing import Generic, TypeVar, Optional, Any, Type
from typing_extensions import Literal

from pydantic.generics import GenericModel


TypeT = TypeVar('TypeT')
AttributesT = TypeVar('AttributesT')
class RequestDataModel(GenericModel, Generic[TypeT, AttributesT]):
    type: TypeT
    attributes: AttributesT


DataT = TypeVar('DataT')
class RequestModel(GenericModel, Generic[DataT]):
    data: DataT


def JsonApiRequest(type_string: str, attributes_model: Any) -> Type[RequestModel]:
    return RequestModel[
        RequestDataModel[
            Literal[type_string],
            attributes_model,
        ],
    ]
