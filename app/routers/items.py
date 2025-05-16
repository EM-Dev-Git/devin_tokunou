from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, description=f"Item {item_id} not found")
    return fake_items_db[item_id]

@router.post("/")
async def create_item(item_id: str, name: str):
    if item_id in fake_items_db:
        raise HTTPException(status_code=400, description=f"Item {item_id} already exists")
    fake_items_db[item_id] = {"name": name}
    return {"item_id": item_id, "name": name}
