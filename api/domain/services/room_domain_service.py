from typing import Dict, Any, Optional, List
from django.utils import timezone


class RoomDomainService:
    """
    Domain service for room-related business logic
    """

    @staticmethod
    def validate_room_capacity(capacity: int) -> None:
        """
        Validate room capacity
        """
        if not isinstance(capacity, int):
            try:
                capacity = int(capacity)
            except (ValueError, TypeError):
                raise ValueError("Capacity must be a valid number")

        if capacity <= 0:
            raise ValueError("Room capacity must be greater than 0")

        if capacity > 1000:
            raise ValueError("Room capacity cannot exceed 1000 people")

    @staticmethod
    def validate_room_name_uniqueness(
        name: str, location_id: str, exclude_room_id: Optional[str] = None
    ) -> bool:
        """
        Validate room name uniqueness within a location
        """

        from ...infrastructure.repositories.django_room_repository import (
            DjangoRoomRepository,
        )

        repository = DjangoRoomRepository()
        return repository.check_name_uniqueness(name, location_id, exclude_room_id)

    @staticmethod
    def has_active_bookings(room) -> bool:
        """
        Check if room has active bookings
        """

        from ...infrastructure.repositories.django_room_repository import (
            DjangoRoomRepository,
        )

        repository = DjangoRoomRepository()
        now = timezone.now()

        bookings = repository.get_bookings_for_room(room.id, start_date=now)
        return len(bookings) > 0

    @staticmethod
    def check_room_availability(
        room, start_date, end_date, exclude_booking_id: Optional[str] = None
    ) -> bool:
        """
        Check if room is available for a given time period
        """
        conflicts = RoomDomainService.get_conflicting_bookings(
            room, start_date, end_date, exclude_booking_id
        )
        return len(conflicts) == 0

    @staticmethod
    def get_conflicting_bookings(
        room, start_date, end_date, exclude_booking_id: Optional[str] = None
    ) -> List:
        """
        Get bookings that conflict with the given time range
        """

        from ...infrastructure.repositories.django_booking_repository import (
            DjangoBookingRepository,
        )

        repository = DjangoBookingRepository()
        return repository.get_conflicting_bookings(
            room.id, start_date, end_date, exclude_booking_id
        )

    @staticmethod
    def validate_room_name_format(name: str) -> None:
        """
        Validate room name format
        """
        if not name or not name.strip():
            raise ValueError("Room name is required")

        name = name.strip()
        if len(name) < 2:
            raise ValueError("Room name must have at least 2 characters")

        if len(name) > 100:
            raise ValueError("Room name cannot exceed 100 characters")

    @staticmethod
    def validate_room_description(description: str) -> None:
        """
        Validate room description
        """
        if description and len(description) > 500:
            raise ValueError("Room description cannot exceed 500 characters")

    @staticmethod
    def get_room_utilization_stats(room) -> Dict[str, Any]:
        """
        Calculate room utilization statistics
        """

        from ...infrastructure.repositories.django_room_repository import (
            DjangoRoomRepository,
        )

        repository = DjangoRoomRepository()
        now = timezone.now()

        all_bookings = repository.get_bookings_for_room(room.id)

        stats = {
            "total_bookings": len(all_bookings),
            "active_bookings": 0,
            "future_bookings": 0,
            "past_bookings": 0,
            "average_duration_hours": 0,
            "most_frequent_user": None,
        }

        total_duration_hours = 0
        user_booking_count = {}

        for booking in all_bookings:
            if booking.start_date <= now <= booking.end_date:
                stats["active_bookings"] += 1
            elif booking.end_date < now:
                stats["past_bookings"] += 1
            elif booking.start_date > now:
                stats["future_bookings"] += 1

            duration = booking.end_date - booking.start_date
            total_duration_hours += duration.total_seconds() / 3600

            if booking.manager and booking.manager.name:
                manager_name = booking.manager.name
                user_booking_count[manager_name] = (
                    user_booking_count.get(manager_name, 0) + 1
                )

        if len(all_bookings) > 0:
            stats["average_duration_hours"] = round(
                total_duration_hours / len(all_bookings), 2
            )

        if user_booking_count:
            stats["most_frequent_user"] = max(
                user_booking_count, key=user_booking_count.get
            )

        return stats
