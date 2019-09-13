
from typing import Mapping, Optional

from pydantic import BaseModel

class RelationshipModel(BaseModel):
    links: Optional[dict]
    data: Optional[dict]
    meta: Optional[dict]

RelationshipsType = Mapping[str, RelationshipModel]

