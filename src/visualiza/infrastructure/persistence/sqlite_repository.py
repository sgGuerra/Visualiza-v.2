from typing import Optional

from src.visualiza.domain.models.user_model import User
from src.visualiza.domain.repositories.user_repository import AbstractUserRepository


class SQLiteUserRepository(AbstractUserRepository):
    """
    Concrete implementation of the user repository using a simple
    in-memory storage for the MVP. This will be replaced with
    actual SQLite database logic.
    """
    _user: Optional[User] = None

    def add(self, user: User) -> None:
        print(f"DEBUG: Adding user {user.name} to in-memory repository.")
        self.__class__._user = user

    def get(self) -> Optional[User]:
        print(f"DEBUG: Getting user from in-memory repository.")
        return self.__class__._user
