"""Middleware for the app."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]


def register_middleware(app: FastAPI) -> None:
    """Register middleware."""
    # Requirements for slowapi middleware
    app.state.limiter = limiter

    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

    # TODO: Add Method not found response

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[
            "X-Total",
            "X-Pages",
            "X-Page",
            "X-Next",
            "X-Prev",
            "X-Limit",
            "X-Offset",
        ],
    )
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
