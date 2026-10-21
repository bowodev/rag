from app.cmd.api.routes.internal import memberships, tenants, users
from fastapi import APIRouter

router = APIRouter(prefix="/internal")

router.include_router(tenants.router)
router.include_router(users.router)
router.include_router(memberships.router)
