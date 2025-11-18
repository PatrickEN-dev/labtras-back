from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ...domain.entities.room import Room


class RoomRepositoryInterface(ABC):
    """
    Repository interface for Room entity
    """

    @abstractmethod
    def get_by_id(self, room_id: str) -> Optional[Room]:
        """Get a room by its ID"""
        pass

    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Room]:
        """Get all rooms with optional filters"""
        pass

    @abstractmethod
    def create(self, room_data: Dict[str, Any]) -> Room:
        """Create a new room"""
        pass

    @abstractmethod
    def update(self, room_id: str, room_data: Dict[str, Any]) -> Optional[Room]:
        """Update an existing room"""
        pass

    @abstractmethod
    def soft_delete(self, room_id: str) -> bool:
        """Soft delete a room"""
        pass

    @abstractmethod
    def get_by_location(self, location_id: str) -> List[Room]:
        """Get all rooms for a specific location"""
        pass

    @abstractmethod
    def get_available_rooms(
        self, start_date: Any, end_date: Any, location_id: Optional[str] = None
    ) -> List[Room]:
        """Get available rooms for a time period"""
        pass

    @abstractmethod
    def check_name_uniqueness(
        self, name: str, location_id: str, exclude_room_id: Optional[str] = None
    ) -> bool:
        """Check if room name is unique within a location"""
        pass

    @abstractmethod
    def has_active_bookings(self, room_id: str) -> bool:
        """Check if room has any active bookings"""
        pass

    @abstractmethod
    def get_room_bookings_count(self, room_id: str) -> Dict[str, int]:
        """Get booking statistics for a room"""
        pass
