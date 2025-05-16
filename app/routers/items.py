from fastapi import APIRouter, HTTPException, Request
from app.modules.item import get_all_items, get_item_by_id, create_new_item
from app.schemas.item import ItemResponse, ItemsResponse
from app.utils.logger import api_logger

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items(request: Request):
    api_logger.info(f"Request to get all items - Request ID: {request.state.request_id}")
    return get_all_items()

@router.get("/{item_id}")
async def read_item(item_id: str, request: Request):
    api_logger.info(f"Request to get item {item_id} - Request ID: {request.state.request_id}")
    
    try:
        item = get_item_by_id(item_id)
        api_logger.info(f"Item {item_id} retrieved successfully - Request ID: {request.state.request_id}")
        return item
    except HTTPException as e:
        api_logger.warning(f"Item {item_id} not found - Request ID: {request.state.request_id}")
        raise

@router.post("/", response_model=ItemResponse)
async def create_item(item_id: str, name: str, request: Request):
    api_logger.info(f"Request to create item {item_id} - Request ID: {request.state.request_id}")
    
    try:
        new_item = create_new_item(item_id, name)
        api_logger.info(f"Item {item_id} created successfully - Request ID: {request.state.request_id}")
        return new_item
    except HTTPException as e:
        api_logger.warning(f"Failed to create item {item_id} - Request ID: {request.state.request_id}")
        raise
