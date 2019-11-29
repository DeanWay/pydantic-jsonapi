
from typing import Mapping, Optional, Union

from pydantic import BaseModel
from pydantic_jsonapi.resource_linkage import ResourceLinkage
from pydantic_jsonapi.resource_links import ResourceLinks


class RequestRelationshipModel(BaseModel):
    data: ResourceLinkage

RequestRelationshipsType = Mapping[str, RequestRelationshipModel]
RequestRelationshipsType.__doc__ = "https://jsonapi.org/format/#crud-creating"


class ResponseRelationshipModel(BaseModel):
    links: Optional[ResourceLinks]
    data: ResourceLinkage
    meta: Optional[dict]

ResponseRelationshipsType = Mapping[str, ResponseRelationshipModel]
ResponseRelationshipsType.__doc__ = "https://jsonapi.org/format/#document-resource-object-relationships"
