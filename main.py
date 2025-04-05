"""main.py."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers.router import app_router
from config.settings import settings
from lifespan import lifespan
from shared.utils.handlers import register_exception_handlers
from shared.utils.middleware import register_middleware

app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
register_middleware(app)
app.include_router(app_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "App is running!"}


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs() -> RedirectResponse:
    """Redirect to docs."""
    return RedirectResponse(url="/docs")
