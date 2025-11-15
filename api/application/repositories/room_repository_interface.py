from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

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
