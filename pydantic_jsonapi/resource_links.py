from typing import Mapping, Union

from pydantic import BaseModel


class LinkHref(BaseModel):
    href: str
    meta: dict

Link = Union[str, LinkHref]
ResourceLinks = Mapping[str, Link]
