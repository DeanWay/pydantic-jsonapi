
from typing import Mapping, Optional

from pydantic import BaseModel
from pydantic_jsonapi.links import LinksType


class RelationshipModel(BaseModel):
    links: Optional[LinksType]
    data: Optional[dict]
    meta: Optional[dict]

RelationshipsType = Mapping[str, RelationshipModel]

