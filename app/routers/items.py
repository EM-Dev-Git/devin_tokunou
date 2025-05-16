from fastapi import APIRouter, HTTPException, Request
from app.utils.logger import api_logger

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items(request: Request):
    api_logger.info(f"Request to get all items - Request ID: {request.state.request_id}")
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str, request: Request):
    api_logger.info(f"Request to get item {item_id} - Request ID: {request.state.request_id}")
    
    if item_id not in fake_items_db:
        api_logger.warning(f"Item {item_id} not found - Request ID: {request.state.request_id}")
        raise HTTPException(status_code=404, description=f"Item {item_id} not found")
    
    api_logger.info(f"Item {item_id} retrieved successfully - Request ID: {request.state.request_id}")
    return fake_items_db[item_id]

@router.post("/")
async def create_item(item_id: str, name: str, request: Request):
    api_logger.info(f"Request to create item {item_id} - Request ID: {request.state.request_id}")
    
    if item_id in fake_items_db:
        api_logger.warning(f"Item {item_id} already exists - Request ID: {request.state.request_id}")
        raise HTTPException(status_code=400, description=f"Item {item_id} already exists")
    
    fake_items_db[item_id] = {"name": name}
    api_logger.info(f"Item {item_id} created successfully - Request ID: {request.state.request_id}")
    return {"item_id": item_id, "name": name}
