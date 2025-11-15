"""
Domain Services - Complex business logic that doesn't belong to a single entity

Available Services:
- BookingDomainService: Complex booking validation and business rules
- RoomDomainService: Room availability, capacity validation, and utilization stats
- ManagerDomainService: Manager validation, uniqueness checks, and statistics
"""

from .booking_domain_service import BookingDomainService
from .room_domain_service import RoomDomainService
from .manager_domain_service import ManagerDomainService

__all__ = ["BookingDomainService", "RoomDomainService", "ManagerDomainService"]
