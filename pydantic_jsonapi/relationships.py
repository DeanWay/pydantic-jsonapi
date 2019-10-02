
from typing import Mapping, Optional, Union

from pydantic import BaseModel
from pydantic_jsonapi.links import LinksType


class RelationshipModel(BaseModel):
    links: Optional[LinksType]
    data: Optional[Union[list, dict]]
    meta: Optional[dict]

RelationshipsType = Mapping[str, RelationshipModel]

