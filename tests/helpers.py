from pydantic import BaseModel
from pydantic_jsonapi import JsonApiRequest

class ItemModel(BaseModel):
    name: str
    quantity: int
    price: float

class ItemModelWithOrmMode(BaseModel):
    name: str
    quantity: int
    price: float
    class Config:
        orm_mode = True

item_type_name = 'item'
ItemRequest = JsonApiRequest(item_type_name, ItemModel)
