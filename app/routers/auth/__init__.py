from fastapi import APIRouter
from app.routers.auth.ms_graph import router as ms_graph_router

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

router.include_router(ms_graph_router)
