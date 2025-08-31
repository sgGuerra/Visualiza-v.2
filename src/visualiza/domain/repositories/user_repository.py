from abc import ABC, abstractmethod
from typing import Optional

from src.visualiza.domain.models.user_model import User


class AbstractUserRepository(ABC):
    """
    Abstract interface for a user repository.
    Defines the contract for data persistence operations.
    """

    @abstractmethod
    def add(self, user: User) -> None:
        """Adds a new user to the repository."""
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Optional[User]:
        """
        Gets the user from the repository.
        For this MVP, we assume there is only one user profile.
        """
        raise NotImplementedError
