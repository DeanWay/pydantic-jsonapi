from typing import Any
from collections.abc import Mapping, Iterable

def filter_none(d: Any):
    if isinstance(d, dict):
        return {k: filter_none(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [filter_none(item) for item in d]
    return d

