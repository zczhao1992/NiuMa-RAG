from fastapi import APIRouter


from src.api.v1 import (
    chat_router,
    user_router,
    collections_router
)

router = APIRouter(prefix="/api")


router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(chat_router)
router_v1.include_router(user_router)
router_v1.include_router(collections_router)

router.include_router(router_v1)
