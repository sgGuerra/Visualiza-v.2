from dataclasses import dataclass, asdict

@dataclass
class User:
    """Represents a user in the domain."""
    name: str
    age: int
    gender: str
    marital_status: str

    def to_dict(self) -> dict:
        """Serializes the user object to a dictionary."""
        return asdict(self)
