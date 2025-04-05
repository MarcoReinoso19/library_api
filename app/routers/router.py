"""This module contains the API router for the application."""

from fastapi import APIRouter

from app.routers import (
    auth_router,
    author_router,
    inventory_router,
    library_router,
    material_router,
    section_router,
    user_router,
)

app_router = APIRouter()
app_router.include_router(auth_router.router)
app_router.include_router(user_router.router)
app_router.include_router(library_router.router)
app_router.include_router(author_router.router)
app_router.include_router(inventory_router.router)
app_router.include_router(material_router.router)
app_router.include_router(section_router.router)
