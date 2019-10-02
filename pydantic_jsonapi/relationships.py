
from typing import Mapping, Optional, Union

from pydantic import BaseModel
from pydantic_jsonapi.resource_linkage import ResourceLinkage
from pydantic_jsonapi.resource_links import LinksType


class RelationshipModel(BaseModel):
    links: Optional[LinksType]
    data: ResourceLinkage
    meta: Optional[dict]

RelationshipsType = Mapping[str, RelationshipModel]

