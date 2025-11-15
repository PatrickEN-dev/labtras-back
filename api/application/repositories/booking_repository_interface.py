from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ...domain.entities.booking import Booking


class BookingRepositoryInterface(ABC):
    """
    Repository interface for Booking entity
    Defines the contract for data access operations
    """

    @abstractmethod
    def get_by_id(self, booking_id: str) -> Optional[Booking]:
        """Get a booking by its ID"""
        pass

    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Booking]:
        """Get all bookings with optional filters"""
        pass

    @abstractmethod
    def create(self, booking_data: Dict[str, Any]) -> Booking:
        """Create a new booking"""
        pass

    @abstractmethod
    def update(
        self, booking_id: str, booking_data: Dict[str, Any]
    ) -> Optional[Booking]:
        """Update an existing booking"""
        pass

    @abstractmethod
    def soft_delete(self, booking_id: str) -> bool:
        """Soft delete a booking"""
        pass

    @abstractmethod
    def find_conflicts(
        self,
        room_id: str,
        start_date: datetime,
        end_date: datetime,
        exclude_booking_id: Optional[str] = None,
    ) -> List[Booking]:
        """Find conflicting bookings for a time period"""
        pass

    @abstractmethod
    def get_by_room(self, room_id: str) -> List[Booking]:
        """Get all bookings for a specific room"""
        pass

    @abstractmethod
    def get_by_manager(self, manager_id: str) -> List[Booking]:
        """Get all bookings for a specific manager"""
        pass
