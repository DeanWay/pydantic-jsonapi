
from typing import Mapping, Optional, Union

from pydantic import BaseModel
from pydantic_jsonapi.resource_linkage import ResourceLinkage
from pydantic_jsonapi.resource_links import ResourceLinks


class RelationshipModel(BaseModel):
    links: Optional[ResourceLinks]
    data: ResourceLinkage
    meta: Optional[dict]

RelationshipsType = Mapping[str, RelationshipModel]
RelationshipsType.__doc__ = "https://jsonapi.org/format/#document-resource-object-relationships"
