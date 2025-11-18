from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from django import db

from ...domain.entities.location import Location


class LocationRepositoryInterface(ABC):
    """
    Repository interface for Location entity
    """

    @abstractmethod
    def get_by_id(self, location_id: str) -> Optional[Location]:
        """Get a location by its ID"""
        pass

    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Location]:
        """Get all locations with optional filters"""
        pass

    @abstractmethod
    def create(self, location_data: Dict[str, Any]) -> Location:
        """Create a new location"""
        pass

    @abstractmethod
    def update(
        self, location_id: str, location_data: Dict[str, Any]
    ) -> Optional[Location]:
        """Update an existing location"""

        pass

    @abstractmethod
    def soft_delete(self, location_id: str) -> bool:
        """Soft delete a location"""
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Location]:
        """Search locations by name (partial match)"""
        pass

    @abstractmethod
    def get_rooms_by_location(self, location_id: str) -> List[Any]:
        """Get all rooms for a specific location"""
        pass

    @abstractmethod
    def has_active_rooms(self, location_id: str) -> bool:
        """Check if location has any active rooms"""
        pass
