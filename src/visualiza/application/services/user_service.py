from typing import Optional

from src.visualiza.domain.models.user_model import User
from src.visualiza.domain.repositories.user_repository import AbstractUserRepository


class UserApplicationService:
    """
    This service handles the application logic for user-related use cases.
    It orchestrates the domain models and repositories.
    """
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    def register_user(
        self, name: str, age: int, gender: str, marital_status: str
    ) -> User:
        """
        Registers a new user.
        In a real app, this would involve more complex logic like validation,
        checking for duplicates, etc.
        """
        # Business rule: age must be valid (example)
        if not 0 < age < 120:
            raise ValueError("Invalid age provided.")

        user = User(
            name=name,
            age=age,
            gender=gender,
            marital_status=marital_status
        )
        self.user_repository.add(user)
        print(f"DEBUG: User {user.name} registered via application service.")
        return user

    def get_user(self) -> Optional[User]:
        """Retrieves the current user."""
        return self.user_repository.get()
