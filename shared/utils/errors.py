"""
errors.py.

Errors: Define custom exceptions to handle errors in the application.
"""

from typing import Any


class InvalidTokenError(Exception):
    """Exception raised when a token is invalid."""

    def __init__(self, message: str = "Invalid token") -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(self.message)


class EmailError(Exception):
    """Exception raised when an email is invalid."""

    def __init__(self, email: str) -> None:
        """Initialize the exception."""
        self.email = email
        self.message = f"Invalid email: {email}"
        super().__init__(self.message)


class AuthorizationError(Exception):
    """Exception raised when a user does not have the required permissions."""

    def __init__(self, message: str = "Not authorized") -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    """Exception raised when credentials are invalid."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.message = "Invalid credentials"
        super().__init__(self.message)


class NotFoundError(Exception):
    """
    Exception raised when an object is not found.

    Attributes:
        - entity_name (str): The name of the entity.
        - entity_attribute (str): The name of the attribute.
        - attribute_value (int | str): The value of the attribute that was not found.
    """

    def __init__(
        self,
        entity_name: str,
        # entity_attribute: str = None,
        entity_attribute: str = "",
        attribute_value: Any = "",
        # attribute_value: int | str = None,
    ) -> None:
        """Initialize the exception."""
        self.entity_name = entity_name
        self.entity_attribute = entity_attribute
        self.attribute_value = attribute_value

        if not attribute_value:
            self.message = f"{entity_name} not found"

        elif entity_attribute:
            self.message = f"{entity_name} with {entity_attribute}: {str(attribute_value)} not found"
        else:
            self.message = f"{entity_name} with value: {attribute_value} not found"
        super().__init__(self.message)


class EntityAlreadyExistsError(Exception):
    """Exception raised when an entity already exists."""

    def __init__(
        self,
        entity_name: str,
        # attribute_name: int | str = None,
        attribute_value: Any,
        attribute_name: str = "",
    ) -> None:
        """Initialize the exception."""
        self.entity_name = entity_name
        self.attribute_value = attribute_value
        self.attribute_name = attribute_name
        if attribute_name:
            self.message = (
                f"{entity_name} with {attribute_name}: {attribute_value} already exists"
            )
        else:
            self.message = f"{entity_name} with value {attribute_value} already exists"
        # self.message = f'{entity_name} with ({attribute_name if attribute_name else ''}{': ' if attribute_name else ''} {attribute_value}) already exists'
        super().__init__(self.message)


class DeleteError(Exception):
    """Exception raised when an object cannot be deleted."""

    def __init__(self, entity_name: str):
        """Initialize the exception."""
        self.message = f"Error deleting {entity_name}"
        super().__init__(self.message)
