from typing import List, Optional, Dict, Any

from ..repositories.location_repository_interface import LocationRepositoryInterface
from ...domain.entities.location import Location


class CreateLocationUseCase:
    """
    Use Case: Create a new location
    """

    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def execute(self, location_data: Dict[str, Any]) -> Location:
        """
        Execute the use case to create a location
        """
        # 1. Validate input data
        name = location_data.get("name")
        address = location_data.get("address")

        if not name or not name.strip():
            raise ValueError("Location name is required")

        if not address or not address.strip():
            raise ValueError("Location address is required")

        # 2. Check name uniqueness
        existing_location = self.location_repository.get_by_name(name.strip())
        if existing_location:
            raise ValueError(f"Location with name '{name}' already exists")

        # 3. Prepare data for repository
        repository_data = {
            "name": name.strip(),
            "address": address.strip(),
            "description": location_data.get("description", "").strip(),
        }

        # 4. Create location
        return self.location_repository.create(repository_data)


class UpdateLocationUseCase:
    """
    Use Case: Update an existing location
    """

    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def execute(self, location_id: str, update_data: Dict[str, Any]) -> Location:
        """
        Execute the use case to update a location
        """
        # 1. Get existing location
        existing_location = self.location_repository.get_by_id(location_id)
        if not existing_location:
            raise ValueError("Location not found")

        # 2. Validate updates
        if "name" in update_data:
            new_name = update_data["name"]
            if not new_name or not new_name.strip():
                raise ValueError("Location name is required")

            # Check uniqueness only if name is being changed
            if new_name.strip() != existing_location.name:
                existing_with_name = self.location_repository.get_by_name(
                    new_name.strip()
                )
                if existing_with_name:
                    raise ValueError(f"Location with name '{new_name}' already exists")

            update_data["name"] = new_name.strip()

        if "address" in update_data:
            new_address = update_data["address"]
            if not new_address or not new_address.strip():
                raise ValueError("Location address is required")

            update_data["address"] = new_address.strip()

        if "description" in update_data:
            update_data["description"] = update_data["description"].strip()

        # 3. Update location
        updated_location = self.location_repository.update(location_id, update_data)
        if not updated_location:
            raise ValueError("Failed to update location")

        return updated_location


class DeleteLocationUseCase:
    """
    Use Case: Delete a location (soft delete)
    """

    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def execute(self, location_id: str) -> bool:
        """
        Execute the use case to delete a location
        """
        # 1. Get existing location
        existing_location = self.location_repository.get_by_id(location_id)
        if not existing_location:
            raise ValueError("Location not found")

        # 2. Check if location has rooms
        rooms = self.location_repository.get_rooms_by_location(location_id)
        if rooms:
            raise ValueError("Cannot delete location with existing rooms")

        # 3. Delete location
        return self.location_repository.soft_delete(location_id)


class ListLocationsUseCase:
    """
    Use Case: List locations with optional filters
    """

    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def execute(self, filters: Optional[Dict[str, Any]] = None) -> List[Location]:
        """
        Execute the use case to list locations
        """
        return self.location_repository.get_all(filters)


class GetLocationUseCase:
    """
    Use Case: Get a single location by ID
    """

    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def execute(self, location_id: str) -> Optional[Location]:
        """
        Execute the use case to get a location
        """
        return self.location_repository.get_by_id(location_id)


class SearchLocationsUseCase:
    """
    Use Case: Search locations by name
    """

    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def execute(self, name: str) -> List[Location]:
        """
        Search locations by name (partial match)
        """
        if not name or not name.strip():
            return []

        return self.location_repository.search_by_name(name.strip())


class GetLocationWithRoomsUseCase:
    """
    Use Case: Get a location with its rooms
    """

    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def execute(self, location_id: str) -> Dict[str, Any]:
        """
        Execute the use case to get a location with its rooms
        """
        # 1. Get location
        location = self.location_repository.get_by_id(location_id)
        if not location:
            raise ValueError("Location not found")

        # 2. Get rooms for this location
        rooms = self.location_repository.get_rooms_by_location(location_id)

        return {"location": location, "rooms": rooms, "room_count": len(rooms)}
