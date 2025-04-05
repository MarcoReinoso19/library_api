"""decorators.py."""

from collections.abc import Awaitable
from functools import wraps
from typing import Any, Callable

from app.services.auth_service import check_permissions
from app.services.user_service import db_read_user_libraries
from shared.utils.errors import AuthorizationError


def authorize(
    permission_name: str,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Create a Decorator to handle authorization."""

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            library_id = kwargs.get("library_id")
            current_user: Any = kwargs.get("current_user")
            session: Any = kwargs.get("session")
            if not current_user:
                raise AuthorizationError("Not authorized, missing user info")
            if not library_id:
                libraries = db_read_user_libraries(
                    session=session, user_id=current_user.id
                )
                if not libraries:
                    raise AuthorizationError("Not Libraries found for user")
                library_id = libraries[0].id

            if check_permissions(
                permission_name=permission_name,
                library_id=library_id,
                current_user=current_user,
                session=session,
            ):
                return await func(*args, **kwargs)

            raise AuthorizationError

        return wrapper

    return decorator
