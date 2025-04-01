import secrets
from dataclasses import dataclass


@dataclass
class Token:
    id: str
    activity_id: str
    is_scope: bool = False
    is_active: bool = False
    is_concurrent: bool = False
    is_completed: bool = False

    @classmethod
    def from_metadata(cls, activity_id: str, metadata: dict, is_active: bool = False):
        return cls(
            id=f"T{secrets.token_hex(3)}",
            activity_id=activity_id,
            is_scope=metadata.get("isScope", False),
            is_active=is_active,
            is_concurrent=metadata.get("isConcurrent", False),
            is_completed=metadata.get("isCompleted", False),
        )
