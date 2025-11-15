from typing import List, Optional, Dict, Any
from django.utils import timezone

from ..repositories.booking_repository_interface import BookingRepositoryInterface
from ..repositories.room_repository_interface import RoomRepositoryInterface
from ..repositories.manager_repository_interface import ManagerRepositoryInterface
from ...domain.services.booking_domain_service import BookingDomainService
from ...domain.entities.booking import Booking


class CreateBookingUseCase:
    """
    Use Case: Create a new booking
    Orchestrates the booking creation process
    """

    def __init__(
        self,
        booking_repository: BookingRepositoryInterface,
        room_repository: RoomRepositoryInterface,
        manager_repository: ManagerRepositoryInterface,
    ):
        self.booking_repository = booking_repository
        self.room_repository = room_repository
        self.manager_repository = manager_repository
        self.domain_service = BookingDomainService()

    def execute(self, booking_data: Dict[str, Any]) -> Booking:
        """
        Execute the use case to create a booking
        """
        # 1. Validate input data structure
        room_id = booking_data.get("room")
        manager_id = booking_data.get("manager")
        start_date = booking_data.get("start_date")
        end_date = booking_data.get("end_date")
        coffee_option = booking_data.get("coffee_option", False)
        coffee_quantity = booking_data.get("coffee_quantity")

        # 2. Validate entities exist
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        manager = self.manager_repository.get_by_id(manager_id)
        if not manager:
            raise ValueError("Manager not found")

        # 3. Apply domain rules
        BookingDomainService.validate_booking_time_rules(start_date, end_date)
        BookingDomainService.validate_coffee_requirements(
            coffee_option, coffee_quantity
        )

        # 4. Check room availability using RoomDomainService
        from ...domain.services.room_domain_service import RoomDomainService

        if not RoomDomainService.check_room_availability(room, start_date, end_date):
            conflicts = RoomDomainService.get_conflicting_bookings(
                room, start_date, end_date
            )
            conflict_info = [
                f"Conflict with booking from {c.start_date} to {c.end_date} by {c.manager.name if c.manager else 'Unknown'}"
                for c in conflicts
            ]
            raise ValueError(
                f"Room is not available for the requested time. {'; '.join(conflict_info)}"
            )

        # 5. Prepare data for repository
        repository_data = {
            "room_id": room_id,
            "manager_id": manager_id,
            "start_date": start_date,
            "end_date": end_date,
            "coffee_option": coffee_option,
            "coffee_quantity": coffee_quantity,
            "coffee_description": booking_data.get("coffee_description"),
        }

        # 6. Create booking
        return self.booking_repository.create(repository_data)


class UpdateBookingUseCase:
    """
    Use Case: Update an existing booking
    """

    def __init__(
        self,
        booking_repository: BookingRepositoryInterface,
        room_repository: RoomRepositoryInterface,
        manager_repository: ManagerRepositoryInterface,
    ):
        self.booking_repository = booking_repository
        self.room_repository = room_repository
        self.manager_repository = manager_repository
        self.domain_service = BookingDomainService()

    def execute(self, booking_id: str, update_data: Dict[str, Any]) -> Booking:
        """
        Execute the use case to update a booking
        """
        # 1. Get existing booking
        existing_booking = self.booking_repository.get_by_id(booking_id)
        if not existing_booking:
            raise ValueError("Booking not found")

        # 2. Check if booking can be modified
        if not BookingDomainService.can_modify_booking(existing_booking):
            raise ValueError(
                "Booking cannot be modified (may have already started or ended)"
            )

        # 3. Validate new data if provided
        start_date = update_data.get("start_date", existing_booking.start_date)
        end_date = update_data.get("end_date", existing_booking.end_date)
        coffee_option = update_data.get("coffee_option", existing_booking.coffee_option)
        coffee_quantity = update_data.get(
            "coffee_quantity", existing_booking.coffee_quantity
        )

        # 4. Apply domain rules
        BookingDomainService.validate_booking_time_rules(start_date, end_date)
        BookingDomainService.validate_coffee_requirements(
            coffee_option, coffee_quantity
        )

        # 5. Check room availability (excluding current booking)
        room_id = update_data.get("room", existing_booking.room_id)
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        from ...domain.services.room_domain_service import RoomDomainService

        if not RoomDomainService.check_room_availability(
            room, start_date, end_date, booking_id
        ):
            raise ValueError("Room is not available for the requested time")

        # 6. Prepare update data
        repository_data = {}
        for key, value in update_data.items():
            if key in ["room", "manager"]:
                repository_data[f"{key}_id"] = value
            else:
                repository_data[key] = value

        # 7. Update booking
        updated_booking = self.booking_repository.update(booking_id, repository_data)
        if not updated_booking:
            raise ValueError("Failed to update booking")

        return updated_booking


class CancelBookingUseCase:
    """
    Use Case: Cancel (soft delete) a booking
    """

    def __init__(self, booking_repository: BookingRepositoryInterface):
        self.booking_repository = booking_repository
        self.domain_service = BookingDomainService()

    def execute(self, booking_id: str) -> bool:
        """
        Execute the use case to cancel a booking
        """
        # 1. Get existing booking
        existing_booking = self.booking_repository.get_by_id(booking_id)
        if not existing_booking:
            raise ValueError("Booking not found")

        # 2. Check if booking can be cancelled
        if not BookingDomainService.can_cancel_booking(existing_booking):
            raise ValueError("Booking cannot be cancelled (may have already ended)")

        # 3. Cancel booking
        return self.booking_repository.soft_delete(booking_id)


class ListBookingsUseCase:
    """
    Use Case: List bookings with optional filters
    """

    def __init__(self, booking_repository: BookingRepositoryInterface):
        self.booking_repository = booking_repository

    def execute(self, filters: Optional[Dict[str, Any]] = None) -> List[Booking]:
        """
        Execute the use case to list bookings
        """
        return self.booking_repository.get_all(filters)

    def execute_by_room(self, room_id: str) -> List[Booking]:
        """
        Get bookings for a specific room
        """
        return self.booking_repository.get_by_room(room_id)

    def execute_by_manager(self, manager_id: str) -> List[Booking]:
        """
        Get bookings for a specific manager
        """
        return self.booking_repository.get_by_manager(manager_id)


class GetBookingUseCase:
    """
    Use Case: Get a single booking by ID
    """

    def __init__(self, booking_repository: BookingRepositoryInterface):
        self.booking_repository = booking_repository

    def execute(self, booking_id: str) -> Optional[Booking]:
        """
        Execute the use case to get a booking
        """
        return self.booking_repository.get_by_id(booking_id)
