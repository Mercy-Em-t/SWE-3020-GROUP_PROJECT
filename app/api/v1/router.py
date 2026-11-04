from fastapi import APIRouter
from app.api.v1.endpoints import auth, savings, loans, audit, members

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(savings.router)
api_router.include_router(loans.router)
api_router.include_router(audit.router)
api_router.include_router(members.router)
