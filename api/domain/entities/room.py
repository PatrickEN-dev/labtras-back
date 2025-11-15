from typing import Optional
from datetime import datetime
import uuid


class Room:
    """
    Domain Entity: Room
    Represents a bookable room within a location
    """

    def __init__(
        self,
        id: str = None,
        name: str = None,
        capacity: Optional[int] = None,
        location_id: str = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self.location_id = location_id
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        return self.name or f"Room {self.id}"

    @property
    def is_active(self) -> bool:
        """Domain method to check if room is active"""
        return self.deleted_at is None

    def can_be_deleted(self, has_active_bookings: bool = False) -> bool:
        """Domain rule: Room can only be deleted if it has no active bookings"""
        return not has_active_bookings

    def mark_as_deleted(self, deleted_at: datetime = None) -> None:
        """Domain method to soft delete room"""
        self.deleted_at = deleted_at or datetime.now()

    def update_info(
        self,
        name: str = None,
        capacity: int = None,
        description: str = None,
        location_id: str = None,
    ) -> None:
        """Domain method to update room information"""
        if name is not None:
            self.name = name
        if capacity is not None:
            self.capacity = capacity
        if description is not None:
            self.description = description
        if location_id is not None:
            self.location_id = location_id
        self.updated_at = datetime.now()

    def validate_capacity(self, required_capacity: int) -> bool:
        """Domain rule: Validate if room can accommodate required capacity"""
        if not self.capacity:
            return True  # No capacity limit set
        return self.capacity >= required_capacity
