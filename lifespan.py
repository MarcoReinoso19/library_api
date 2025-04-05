"""lifespan.py."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.author import DBAuthor
from app.models.inventory import DBInventory
from app.models.library import DBLibrary
from app.models.library_users import DBLibraryUser
from app.models.material import DBMaterial
from app.models.permission import DBPermission
from app.models.role import DBRole
from app.models.role_permissions import DBRolePermission
from app.models.section import DBSection
from app.models.user import DBUser
from app.models.user_roles import DBUserRole
from db.database import create_db_and_tables, engine
from shared.utils.deps import commit_and_refresh
from shared.utils.enums import MaterialType

entities: dict[str, Any] = {
    "user1": DBUser(
        username="Marco_Reinoso",
        password="$2b$12$5DlIcgEec5kddvNSbX9N/OlFzvxQZafQb9k8jh73LDxeyBx45LCne",
        email="example@email.com",
    ),
    "library1": DBLibrary(
        name="Biblioteca 1",
        address="Calle 1, Ciudad 1",
    ),
    "library2": DBLibrary(
        name="Biblioteca 2",
        address="Calle 2, Ciudad 2",
    ),
    "library3": DBLibrary(
        name="Biblioteca 3",
        address="Calle 3, Ciudad 3",
    ),
    "library4": DBLibrary(
        name="Biblioteca 4",
        address="Calle 4, Ciudad 4",
    ),
    "rol1": DBRole(
        name="Admin",
        code="AD",
        description="Administrador",
    ),
    "rol2": DBRole(
        name="User",
        code="US",
        description="Usuario",
    ),
    "rol3": DBRole(
        name="Owner",
        code="OW",
        description="Propietario",
    ),
    "permission1": DBPermission(
        name="user:create",
        code="UC",
        description="Crear usuario",
    ),
    "permission2": DBPermission(
        name="user:read",
        code="UR",
        description="Leer usuario",
    ),
    "permission3": DBPermission(
        name="user:update",
        code="UU",
        description="Actualizar usuario",
    ),
    "permission4": DBPermission(
        name="user:delete",
        code="UD",
        description="Eliminar usuario",
    ),
    "permission5": DBPermission(
        name="library:create",
        code="LC",
        description="Crear biblioteca",
    ),
    "permission6": DBPermission(
        name="library:read",
        code="LR",
        description="Leer biblioteca",
    ),
    "permission7": DBPermission(
        name="library:update",
        code="LU",
        description="Actualizar biblioteca",
    ),
    "permission8": DBPermission(
        name="library:delete",
        code="LD",
        description="Eliminar biblioteca",
    ),
    "permission9": DBPermission(
        name="material:create",
        code="MC",
        description="Crear material",
    ),
    "permission10": DBPermission(
        name="material:read",
        code="MR",
        description="Leer material",
    ),
    "permission11": DBPermission(
        name="material:update",
        code="MU",
        description="Actualizar material",
    ),
    "permission12": DBPermission(
        name="material:delete",
        code="MD",
        description="Eliminar material",
    ),
    "permission13": DBPermission(
        name="inventory:create",
        code="IC",
        description="Crear inventario",
    ),
    "permission14": DBPermission(
        name="inventory:read",
        code="IR",
        description="Leer inventario",
    ),
    "permission15": DBPermission(
        name="inventory:update",
        code="IU",
        description="Actualizar inventario",
    ),
    "permission16": DBPermission(
        name="inventory:delete",
        code="ID",
        description="Eliminar inventario",
    ),
    "user_role1": DBUserRole(
        user_id=1,
        role_id=1,
        library_id=1,
    ),
    "user_role2": DBUserRole(
        user_id=1,
        role_id=2,
        library_id=2,
    ),
    "user_library1": DBLibraryUser(
        user_id=1,
        library_id=1,
    ),
    "user_library2": DBLibraryUser(
        user_id=1,
        library_id=2,
    ),
    "user_library3": DBLibraryUser(
        user_id=1,
        library_id=3,
    ),
    "role_permission1": DBRolePermission(
        role_id=1,
        permission_id=1,
    ),
    "role_permission2": DBRolePermission(
        role_id=1,
        permission_id=2,
    ),
    "role_permission3": DBRolePermission(
        role_id=2,
        permission_id=3,
    ),
    "role_permission4": DBRolePermission(
        role_id=3,
        permission_id=4,
    ),
    "role_permission5": DBRolePermission(
        role_id=1,
        permission_id=5,
    ),
    "role_permission6": DBRolePermission(
        role_id=1,
        permission_id=11,
    ),
    "role_permission7": DBRolePermission(
        role_id=1,
        permission_id=7,
    ),
    "role_permission8": DBRolePermission(
        role_id=1,
        permission_id=13,
    ),
    "role_permission9": DBRolePermission(
        role_id=1,
        permission_id=14,
    ),
    "role_permission10": DBRolePermission(
        role_id=1,
        permission_id=15,
    ),
    "role_permission11": DBRolePermission(
        role_id=1,
        permission_id=16,
    ),
    "section1": DBSection(
        name="Sección de Historia ",
        capacity=100,
    ),
    "section2": DBSection(
        name="Sección de Matemáticas",
        capacity=100,
    ),
    "author1": DBAuthor(
        name="Autor 1",
    ),
    "author2": DBAuthor(
        name="Autor 2",
    ),
    "material1": DBMaterial(
        type=MaterialType.BOOK.name,
        title="Libro 1",
        cod_ref="1234567890",
        price=108000,
        isbn="978-3-16-148410-0",
        description="Descripción del libro 1",
        author_id=1,
        section_id=1,
    ),
    "material2": DBMaterial(
        type=MaterialType.MAGAZINE.name,
        title="Revista 1",
        cod_ref="0987654321",
        price=500000,
        issn="1234-5678",
        description="Descripción de la revista 1",
        author_id=2,
        section_id=2,
    ),
    "material3": DBMaterial(
        type=MaterialType.NEWSPAPER.name,
        title="Periódico 1",
        cod_ref="1122334455",
        price=200000,
        description="Descripción del periódico 1",
        author_id=1,
        section_id=1,
    ),
    "inventory1": DBInventory(
        stock=10,
        material_id=1,
        library_id=1,
    ),
    "inventory2": DBInventory(
        stock=5,
        material_id=2,
        library_id=2,
    ),
    "inventory3": DBInventory(
        stock=20,
        material_id=3,
        library_id=3,
    ),
    "inventory4": DBInventory(
        stock=15,
        material_id=1,
        library_id=2,
    ),
    "inventory5": DBInventory(
        stock=150,
        material_id=2,
        library_id=4,
    ),
}


@asynccontextmanager
async def lifespan(life_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager."""
    life_app.version = "0.1.0"
    create_db_and_tables()
    session: Session | None = None
    try:
        with Session(engine) as session:
            # doc = session.get(DBDocumentType, 1)
            book = session.get(DBUser, 1)
            if book is not None:
                print("Exitoso".center(100, "-"))
            else:
                for entity in entities.values():
                    create_entity(session, entity)

                session.close_all()
            yield
    except SQLAlchemyError as e:
        if session is not None:
            session.rollback()
            print(f"\033[91mERROR EN LIFESPAN {e}\033[0m".center(100, "/"))
        raise e
    finally:
        if session is not None:
            session.close()


def create_entity(
    session: Session, entity_object: Any, entity_type: type[Any] | None = None
) -> Any:
    """Create an generic entity."""
    new_entity = entity_object
    if isinstance(entity_object, dict) and entity_type is not None:
        new_entity = entity_type(**entity_object)
    return commit_and_refresh(session, new_entity)
