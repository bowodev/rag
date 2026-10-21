from app.cmd.api.routes import auth, health, me, tenants
from app.cmd.api.routes.internal import router as internal_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(me.router)
api_router.include_router(tenants.router)
api_router.include_router(internal_router)
