from pydantic import BaseModel
from typing import Dict, Optional

class Item(BaseModel):
    name: str

class ItemResponse(BaseModel):
    item_id: str
    name: str

class ItemsResponse(BaseModel):
    items: Dict[str, Item]
