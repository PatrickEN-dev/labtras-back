from typing import List, Optional, Dict, Any

from ..repositories.room_repository_interface import RoomRepositoryInterface
from ..repositories.location_repository_interface import LocationRepositoryInterface
from ...domain.services.room_domain_service import RoomDomainService
from ...domain.entities.room import Room


class CreateRoomUseCase:
    """
    Use Case: Create a new room
    """

    def __init__(
        self,
        room_repository: RoomRepositoryInterface,
        location_repository: LocationRepositoryInterface,
    ):
        self.room_repository = room_repository
        self.location_repository = location_repository
        self.domain_service = RoomDomainService()

    def execute(self, room_data: Dict[str, Any]) -> Room:
        """
        Execute the use case to create a room
        """
        # 1. Validate input data
        location_id = room_data.get("location")
        name = room_data.get("name")
        capacity = room_data.get("capacity")

        # 2. Validate location exists
        location = self.location_repository.get_by_id(location_id)
        if not location:
            raise ValueError("Location not found")

        # 3. Apply domain rules
        from ...domain.services.room_domain_service import RoomDomainService

        RoomDomainService.validate_room_capacity(capacity)
        RoomDomainService.validate_room_name_format(name)

        # 4. Check name uniqueness within location
        if not RoomDomainService.validate_room_name_uniqueness(name, location_id):
            raise ValueError(
                f"Room with name '{name}' already exists in this location"
            )  # 5. Prepare data for repository
        repository_data = {
            "location_id": location_id,
            "name": name,
            "capacity": capacity,
            "description": room_data.get("description"),
        }

        # 6. Create room
        return self.room_repository.create(repository_data)


class UpdateRoomUseCase:
    """
    Use Case: Update an existing room
    """

    def __init__(
        self,
        room_repository: RoomRepositoryInterface,
        location_repository: LocationRepositoryInterface,
    ):
        self.room_repository = room_repository
        self.location_repository = location_repository
        self.domain_service = RoomDomainService()

    def execute(self, room_id: str, update_data: Dict[str, Any]) -> Room:
        """
        Execute the use case to update a room
        """
        # 1. Get existing room
        existing_room = self.room_repository.get_by_id(room_id)
        if not existing_room:
            raise ValueError("Room not found")

        # 2. Validate updates
        from ...domain.services.room_domain_service import RoomDomainService

        if "capacity" in update_data:
            RoomDomainService.validate_room_capacity(update_data["capacity"])

        if "name" in update_data:
            RoomDomainService.validate_room_name_format(update_data["name"])

        if "description" in update_data:
            RoomDomainService.validate_room_description(update_data["description"])

        # 3. Check name uniqueness if name is being changed
        if "name" in update_data:
            new_name = update_data["name"]
            location_id = update_data.get("location", existing_room.location_id)

            if new_name != existing_room.name:
                if not RoomDomainService.validate_room_name_uniqueness(
                    new_name, location_id, room_id
                ):
                    raise ValueError(
                        f"Room with name '{new_name}' already exists in this location"
                    )

        # 4. Validate location if being changed
        if "location" in update_data:
            location = self.location_repository.get_by_id(update_data["location"])
            if not location:
                raise ValueError("Location not found")

        # 5. Prepare update data
        repository_data = {}
        for key, value in update_data.items():
            if key == "location":
                repository_data["location_id"] = value
            else:
                repository_data[key] = value

        # 6. Update room
        updated_room = self.room_repository.update(room_id, repository_data)
        if not updated_room:
            raise ValueError("Failed to update room")

        return updated_room


class DeleteRoomUseCase:
    """
    Use Case: Delete a room (soft delete)
    """

    def __init__(self, room_repository: RoomRepositoryInterface):
        self.room_repository = room_repository
        self.domain_service = RoomDomainService()

    def execute(self, room_id: str) -> bool:
        """
        Execute the use case to delete a room
        """
        # 1. Get existing room
        existing_room = self.room_repository.get_by_id(room_id)
        if not existing_room:
            raise ValueError("Room not found")

        # 2. Check if room has active bookings
        if RoomDomainService.has_active_bookings(existing_room):
            raise ValueError("Cannot delete room with active bookings")

        # 3. Delete room
        return self.room_repository.soft_delete(room_id)


class ListRoomsUseCase:
    """
    Use Case: List rooms with optional filters
    """

    def __init__(self, room_repository: RoomRepositoryInterface):
        self.room_repository = room_repository

    def execute(self, filters: Optional[Dict[str, Any]] = None) -> List[Room]:
        """
        Execute the use case to list rooms
        """
        return self.room_repository.get_all(filters)

    def execute_by_location(self, location_id: str) -> List[Room]:
        """
        Get rooms for a specific location
        """
        return self.room_repository.get_by_location(location_id)

    def execute_available_rooms(
        self, start_date, end_date, location_id: Optional[str] = None
    ) -> List[Room]:
        """
        Get available rooms for a time period
        """
        return self.room_repository.get_available_rooms(
            start_date, end_date, location_id
        )


class GetRoomUseCase:
    """
    Use Case: Get a single room by ID
    """

    def __init__(self, room_repository: RoomRepositoryInterface):
        self.room_repository = room_repository

    def execute(self, room_id: str) -> Optional[Room]:
        """
        Execute the use case to get a room
        """
        return self.room_repository.get_by_id(room_id)


class CheckRoomAvailabilityUseCase:
    """
    Use Case: Check if a room is available for booking
    """

    def __init__(self, room_repository: RoomRepositoryInterface):
        self.room_repository = room_repository
        self.domain_service = RoomDomainService()

    def execute(self, room_id: str, start_date, end_date) -> Dict[str, Any]:
        """
        Execute the use case to check room availability
        """
        # 1. Get room
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        # 2. Check availability
        is_available = RoomDomainService.check_room_availability(
            room, start_date, end_date
        )

        result = {
            "room_id": room_id,
            "start_date": start_date,
            "end_date": end_date,
            "is_available": is_available,
        }

        if not is_available:
            # Get conflicting bookings for details
            conflicts = RoomDomainService.get_conflicting_bookings(
                room, start_date, end_date
            )
            result["conflicts"] = [
                {
                    "booking_id": conflict.id,
                    "start_date": conflict.start_date,
                    "end_date": conflict.end_date,
                    "manager_id": conflict.manager_id,
                }
                for conflict in conflicts
            ]

        return result
