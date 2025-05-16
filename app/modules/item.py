from fastapi import HTTPException
from typing import Dict

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

def get_all_items() -> Dict:
    """Get all items from the database"""
    return fake_items_db

def get_item_by_id(item_id: str) -> Dict:
    """Get a specific item by ID"""
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, description=f"Item {item_id} not found")
    return fake_items_db[item_id]

def create_new_item(item_id: str, name: str) -> Dict:
    """Create a new item in the database"""
    if item_id in fake_items_db:
        raise HTTPException(status_code=400, description=f"Item {item_id} already exists")
    fake_items_db[item_id] = {"name": name}
    return {"item_id": item_id, "name": name}
