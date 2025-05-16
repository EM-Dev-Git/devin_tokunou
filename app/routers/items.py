from fastapi import APIRouter, HTTPException, Request
from app.modules.item import get_all_items, get_item_by_id, create_new_item
from app.schemas.item import ItemResponse, ItemsResponse

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    return get_all_items()

@router.get("/{item_id}")
async def read_item(item_id: str):
    return get_item_by_id(item_id)

@router.post("/", response_model=ItemResponse)
async def create_item(item_id: str, name: str):
    return create_new_item(item_id, name)
