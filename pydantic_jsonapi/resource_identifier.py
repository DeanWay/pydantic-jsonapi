from typing import Optional

from pydantic import BaseModel


class ResourceIdentifier(BaseModel):
    """
    https://jsonapi.org/format/#document-resource-identifier-objects
    """
    id: str
    type: str
    meta: Optional[dict]
