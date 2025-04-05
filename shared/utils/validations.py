import re
from typing import Any, TypeVar

from sqlalchemy import UniqueConstraint, select
from sqlalchemy.orm import Session

from shared.utils.errors import (
    EntityAlreadyExistsError,
    NotFoundError,
)

T = TypeVar("T")


def validate_email_format(email: str) -> bool:
    """Valida que el email tenga un formato correcto."""
    if not email:
        raise ValueError("Email field is required.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError(f"Invalid email format: {email}.")
    return True


def validate_entity_existence(
    session: Session, entity_type: type[T], entity_id: int
) -> T:
    """Valida la existencia de una entidad en la base de datos y la devuelve."""
    if entity_id <= 0:
        raise ValueError(f"ID invalid: {entity_id}.")
    entity = session.get(entity_type, entity_id)
    if not entity:
        raise NotFoundError(entity_type.__name__, "id", entity_id)
    return entity


def validate_unique_constraints(
    session: Session, entity_type: type[Any], entity_object: object
) -> bool:
    """Valida las restricciones de unicidad de una entidad en la base de datos."""
    _validate_entity_unique_constraints(session, entity_type, entity_object)
    _validate_entity_unique_attributes(session, entity_type, entity_object)
    return True


def _get_unique_constraints(entity_type: type[Any]) -> list[list[str]]:
    """Get the unique constraints defined in the entity's table."""
    unique_constraints: list[list[str]] = []

    for constraint in getattr(entity_type, "__table_args__", []):
        if isinstance(constraint, UniqueConstraint):
            unique_constraints.append(constraint.columns.keys())

    return unique_constraints


def _validate_entity_unique_constraints(
    session: Session, entity_type: type[Any], entity_object: object
) -> bool:
    """Check if an entity violates any unique constraint in the database."""
    unique_constraints = _get_unique_constraints(entity_type)

    # Validate each unique constraint
    for constraint in unique_constraints:
        filter_args = {
            col: getattr(entity_object, col, None)
            for col in constraint
            if hasattr(entity_object, col)
        }
        # Skip constraints that cannot be validated due to missing attributes
        if not all(value is not None for value in filter_args.values()):
            continue

        query = session.query(entity_type).filter_by(**filter_args)
        if query.count() > 0:
            raise EntityAlreadyExistsError(
                entity_type.__name__,
                list(filter_args.values()),
                str(list(filter_args.keys())),
            )

    return True


def _validate_entity_unique_attributes(
    session: Session, entity_type: type[Any], entity_object: object
) -> bool:
    """Check if attributes of an entity are unique in the database."""
    is_valid = True
    table = entity_type.__table__

    # Validate each unique attribute
    for column in table.columns:
        if column is not None and column.unique is True:
            res = _validate_unique_attribute(
                session,
                entity_type,
                column.name,
                str(getattr(entity_object, column.name)),
            )
            if not res:
                is_valid = False
    return is_valid


def _validate_unique_attribute(
    session: Session, entity_type: type[Any], attribute_name: str, attribute_value: str
) -> bool:
    """Check if an attribute value is unique in the database."""
    is_unique = True

    # Get the entity with the attribute value to check if it already exists
    entity = session.execute(
        select(entity_type).where(
            getattr(entity_type, attribute_name) == attribute_value
        )
    ).first()

    # If the entity exists, raise an error
    if entity is not None:
        is_unique = False
        raise EntityAlreadyExistsError(
            entity_type.__name__, attribute_value, attribute_name
        )
    return is_unique
