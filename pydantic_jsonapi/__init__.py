from typing import Any

from .request import JsonApiRequest
from .response import JsonApiResponse


def JsonApiModel(type_string: str, attributes_model: Any) -> tuple:
    return (
        JsonApiRequest(type_string, attributes_model),
        JsonApiResponse(type_string, attributes_model)
    )

__all__ = [
    'JsonApiModel',
    'JsonApiRequest',
    'JsonApiResponse',
]
