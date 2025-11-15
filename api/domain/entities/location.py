from typing import Optional
from datetime import datetime
import uuid


class Location:
    """
    Domain Entity: Location
    Represents a physical location where rooms can be found
    """

    def __init__(
        self,
        id: str = None,
        name: str = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.address = address
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        return self.name or f"Location {self.id}"

    @property
    def is_active(self) -> bool:
        """Domain method to check if location is active"""
        return self.deleted_at is None

    def can_be_deleted(self, has_active_rooms: bool = False) -> bool:
        """Domain rule: Location can only be deleted if it has no active rooms"""
        return not has_active_rooms

    def mark_as_deleted(self, deleted_at: datetime = None) -> None:
        """Domain method to soft delete location"""
        self.deleted_at = deleted_at or datetime.now()

    def update_info(
        self, name: str = None, address: str = None, description: str = None
    ) -> None:
        """Domain method to update location information"""
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()
