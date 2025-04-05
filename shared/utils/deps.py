"""deps.py."""

# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

from enum import Enum
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ConfigDict, ValidationError
from sqlalchemy.orm import Session

from app.models.user import DBUser
from app.schemas.token import AccessToken
from config.settings import settings
from db.database import engine
from shared.utils.errors import InvalidCredentialsError, InvalidTokenError


class ConfigModel(BaseModel):
    """
    Clase base para la configuración de los modelos.

    Attributes:
        - model_config : Un objeto de tipo ConfigDict que contiene la configuración del modelo.
            - extra: "forbid" para evitar campos adicionales no definidos en el modelo.
            - from_attributes: True para permitir la inicialización de los datos desde atributos de la instancia.
    """

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class SortEnum(Enum):
    """Clase Enum para definir los valores de ordenación."""

    ASC = "asc"
    DESC = "desc"


class CommonParameters(BaseModel):
    """
    Clase para definir parámetros comunes utilizados en las solicitudes.

    Attributes:
        - q (str | None): Consulta de búsqueda opcional. Si no se proporciona, se establece en None.
        - offset (int): Índice de inicio de la consulta paginada. Por defecto es 0.
        - limit (int): Número máximo de resultados devueltos por la consulta paginada. Por defecto es 30.
    """

    q: str | None = None
    offset: int = 0
    limit: int = 30
    order: SortEnum = SortEnum.ASC
    filter: str | None = None
    filter_value: str | None = None


# Define un parámetro común llamado 'commonParams' que se utilizará en las rutas de FastAPI.
# Se basa en la clase CommonParameters definida anteriormente y depende de las dependencias #especificadas en Depends().
# Esta Anotación se utiliza para indicar que 'commonParams' es un parámetro inyectable que
# puede ser utilizado en las rutas de FastAPI.
CommonParams = Annotated[CommonParameters, Depends()]


def paginate_response_header(
    response: Response, commons: CommonParameters, total: int
) -> None:
    """Add pagination headers to the response."""
    if commons.limit < 0:
        commons.limit = total
    page = (
        (commons.offset + commons.limit) // commons.limit
        if total > 0 and commons.limit != 0
        else 1
    )
    pages = (
        0
        if total <= 0
        else (total + commons.limit - 1) // commons.limit
        if total > commons.limit and commons.limit != 0
        else 1
    )
    next = page + 1 if page < pages else None
    prev = page - 1 if page > 1 else None

    response.headers["X-Total"] = str(total)
    response.headers["X-Pages"] = str(pages)
    response.headers["X-Page"] = str(page)
    response.headers["X-Next"] = str(next)
    response.headers["X-Prev"] = str(prev)
    response.headers["X-Limit"] = str(commons.limit)
    response.headers["X-Offset"] = str(commons.offset)


def commit_and_refresh(db: Session, instance: Any, commit: bool = True) -> Any:
    """
    Commit and refresh an instance in the database.

    If `commit` is True, commit the changes, refresh the instance, and return it.
    If `commit` is False, flush the instance and return it, leaving the transaction open.
    """
    try:
        db.add(instance)
        if commit:
            db.commit()
            db.refresh(instance)
        else:
            db.flush()  # Just flush, no commit
        return instance
    except Exception:
        db.rollback()
        raise


def get_session() -> Any:
    """Get a database session."""
    session = None
    try:
        with Session(engine) as session:
            yield session
    finally:
        if session and session.is_active:
            session.close()


SessionDep = Annotated[Session, Depends(get_session)]


reusable_oauth2: Any = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login",
    scheme_name="JWT",
)

TokenDep = Annotated[reusable_oauth2, Depends()]


async def get_current_user(
    token: str = Depends(reusable_oauth2),
    session: Session = Depends(get_session),
) -> DBUser:
    """Get current user."""
    try:
        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        access_token = AccessToken(**payload)

    except JWTError:
        raise InvalidTokenError
    except ValidationError:
        raise InvalidCredentialsError
    user = session.query(DBUser).filter(DBUser.username == access_token.subject).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUserDep = Annotated[DBUser, Depends(get_current_user)]
