"""handlers.py."""

import logging
from typing import Any

from email_validator import EmailNotValidError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from shared.utils.errors import (
    AuthorizationError,
    DeleteError,
    EmailError,
    EntityAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    NotFoundError,
)

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnusedFunction=false


# Custom exception handlers
def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers for the application."""

    @app.exception_handler(EmailError)
    async def email_exception_handler(
        request: Request, exc: EmailError
    ) -> HTTPException:
        """Handle EmailError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.message,
        ) from exc

    @app.exception_handler(DeleteError)
    async def delete_error_exception_handler(
        request: Request, exc: DeleteError
    ) -> HTTPException:
        """Handle DeleteError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.message,
        ) from exc

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_exception_handler(
        request: Request, exc: InvalidTokenError
    ) -> HTTPException:
        """Handle InvalidTokenError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
        ) from exc

    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(
        request: Request, exc: AuthorizationError
    ) -> HTTPException:
        """Handle AuthorizationError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
        ) from exc

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_exception_handler(
        request: Request, exc: InvalidCredentialsError
    ) -> HTTPException:
        """Handle InvalidCredentialsError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> HTTPException:
        """Handle validation errors."""
        errors: Any = []
        for error in exc.errors():
            errors.append(
                {
                    "loc": error["loc"],
                    "message": error["msg"],
                    "type": error["type"],
                }
            )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": errors},
        )

    @app.exception_handler(ResponseValidationError)
    async def response_validation_exception_handler(
        request: Request, exc: ResponseValidationError
    ) -> HTTPException:
        """Handle validation errors."""
        errors: Any = []
        for error in exc.errors():
            errors.append(
                {
                    "loc": error["loc"],
                    "message": error["msg"],
                    "type": error["type"],
                }
            )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": errors},
        ) from exc

    @app.exception_handler(NotFoundError)
    async def notfound_exception_handler(
        request: Request, exc: NotFoundError
    ) -> HTTPException:
        """Handle NotFoundError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        ) from exc

    @app.exception_handler(EntityAlreadyExistsError)
    async def entity_exists_exception_handler(
        request: Request, exc: EntityAlreadyExistsError
    ) -> HTTPException:
        """Handle EntityAlreadyExistsError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.message,
        ) from exc

    @app.exception_handler(IntegrityError)
    async def integrity_error_exception_handler(
        request: Request, exc: IntegrityError
    ) -> HTTPException:
        """Handle IntegrityError exceptions."""
        if "(psycopg2.errors.UniqueViolation)" in exc.args[0]:
            message = exc.args[0].split("DETAIL:  ")[1].split("\n")[0]
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            )
        raise HTTPException(
            status_code=status.HTTP_306_RESERVED,
            detail=exc.args,
        ) from exc

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request, exc: SQLAlchemyError
    ) -> HTTPException:
        """Handle SQLAlchemy errors."""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.args,
        ) from exc

    @app.exception_handler(EmailNotValidError)
    async def email_not_valid_exception_handler(
        request: Request, exc: EmailNotValidError
    ) -> HTTPException:
        """Handle EmailNotValidError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.args[0],
        ) from exc

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        """Handle HTTP exceptions. Return a JSONResponse with the exception message."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request, exc: ValidationError
    ) -> HTTPException:
        """Handle ValidationError exceptions."""
        logging.error(f"Validation error: {exc.errors()}")

        errors: list[dict[Any, Any]] = [
            {
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"],
            }
            for error in exc.errors()
        ]
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors,
        )

    @app.exception_handler(ValueError)
    async def value_error_exception_handler(
        request: Request, exc: ValueError
    ) -> HTTPException:
        """Handle ValueError exceptions."""
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.args[0] if len(exc.args) > 0 else exc.args,
        ) from exc
