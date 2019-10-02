from typing import Optional

from pydantic import BaseModel


class ResourceIdentifier(BaseModel):
    id: str
    type: str
    meta: Optional[dict]
