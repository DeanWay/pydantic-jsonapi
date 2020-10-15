from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel
from pydantic_jsonapi import JsonApiRequest, JsonApiResponse


# A mock database object
# This could be any form of persistence
@dataclass
class ItemData:
    name: str
    quantity: int
    price: float
    id: str = str(uuid4().hex)
    created_at: datetime = datetime.now()


# Define our Item Request/Response schema
class Item(BaseModel):
    name: str
    quantity: int
    price: float
    class Config:
        orm_mode = True


ITEM_TYPE_NAME = 'item'
ItemRequest = JsonApiRequest(ITEM_TYPE_NAME, Item)
ItemResponse = JsonApiResponse(ITEM_TYPE_NAME, Item)
ItemListResponse = JsonApiResponse(ITEM_TYPE_NAME, Item, use_list=True)

# Simple post method logic
def item_post_method(item_request: ItemRequest) -> ItemResponse:
    attributes = item_request.data.attributes
    item_row = ItemData(**attributes.dict())
    return ItemResponse(
        data=ItemResponse.resource_object(
            id=item_row.id,
            attributes=item_row
        )
    )


def item_list_get_method() -> ItemListResponse:
    item_rows = [
       ItemData(name="apple", quantity=10, price=1.5),
       ItemData(name="orange", quantity=0, price=2.2),
    ]
    return ItemListResponse(
        data=[
            ItemListResponse.resource_object(
                id=item_row.id,
                attributes=item_row
            ) for item_row in item_rows
        ]
    )


# example request
mock_request = {
    'data': {
        'type': 'item',
        'attributes': {
            'name': 'apple',
            'quantity': 10,
            'price': 1.20,
        }
    }
}
response = item_post_method(ItemRequest(**mock_request))
print(response.json(indent=2))
# prints:
# {
#   "data": {
#     "id": "b56ba127bab6459db045d0038a0c06ba",
#     "type": "item",
#     "attributes": {
#       "name": "apple",
#       "quantity": 10,
#       "price": 1.2
#     },
#     "relationships": null
#   },
#   "included": null,
#   "meta": null,
#   "links": null,
#   "errors": null
# }
