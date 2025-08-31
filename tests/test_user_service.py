import sys
import os
import pytest

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.visualiza.application.services.user_service import UserApplicationService
from src.visualiza.infrastructure.persistence.sqlite_repository import SQLiteUserRepository
from src.visualiza.domain.models.user_model import User

@pytest.fixture
def user_service():
    """Fixture to create a UserApplicationService with an in-memory repository."""
    repository = SQLiteUserRepository()
    return UserApplicationService(user_repository=repository)

def test_register_user_and_get_user(user_service: UserApplicationService):
    """
    Tests that a user can be registered and then retrieved.
    """
    # Arrange
    name = "Test User"
    age = 30
    gender = "Test"
    marital_status = "Single"

    # Act
    registered_user = user_service.register_user(
        name=name,
        age=age,
        gender=gender,
        marital_status=marital_status
    )
    retrieved_user = user_service.get_user()

    # Assert
    assert registered_user is not None
    assert retrieved_user is not None
    assert retrieved_user.name == name
    assert retrieved_user.age == age
    assert retrieved_user.gender == gender
    assert retrieved_user.marital_status == marital_status
    assert registered_user == retrieved_user

def test_register_user_with_invalid_age_raises_error(user_service: UserApplicationService):
    """
    Tests that registering a user with an invalid age raises a ValueError.
    """
    # Arrange, Act, and Assert
    with pytest.raises(ValueError, match="Invalid age provided."):
        user_service.register_user(
            name="Test User",
            age=150,  # Invalid age
            gender="Test",
            marital_status="Single"
        )
