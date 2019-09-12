from pydantic import BaseModel


class ItemModel(BaseModel):
    name: str
    quantity: int
    price: float
