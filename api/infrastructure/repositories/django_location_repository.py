from typing import List, Optional, Dict, Any
from django.db import models
from django.utils import timezone

from ...models import Location as LocationModel
from ...application.repositories.location_repository_interface import (
    LocationRepositoryInterface,
)
from ...domain.entities.location import Location


class DjangoLocationRepository(LocationRepositoryInterface):
    """
    Django ORM implementation of LocationRepositoryInterface
    """

    def create(self, data: Dict[str, Any]) -> Location:
        """Create a new location"""
        location_model = LocationModel.objects.create(**data)
        return self._model_to_entity(location_model)

    def get_by_id(self, location_id: str) -> Optional[Location]:
        """Get location by ID"""
        try:
            location_model = LocationModel.objects.get(
                id=location_id, deleted_at__isnull=True
            )
            return self._model_to_entity(location_model)
        except LocationModel.DoesNotExist:
            return None

    def get_by_name(self, name: str) -> Optional[Location]:
        """Get location by name"""
        try:
            location_model = LocationModel.objects.get(
                name__iexact=name, deleted_at__isnull=True
            )
            return self._model_to_entity(location_model)
        except LocationModel.DoesNotExist:
            return None

    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Location]:
        """Get all locations with optional filters"""
        queryset = LocationModel.objects.filter(deleted_at__isnull=True)

        if filters:
            if "name" in filters:
                queryset = queryset.filter(name__icontains=filters["name"])
            if "address" in filters:
                queryset = queryset.filter(address__icontains=filters["address"])

        return [self._model_to_entity(location) for location in queryset]

    def update(self, location_id: str, data: Dict[str, Any]) -> Optional[Location]:
        """Update location"""
        try:
            location_model = LocationModel.objects.get(
                id=location_id, deleted_at__isnull=True
            )
            for key, value in data.items():
                setattr(location_model, key, value)
            location_model.updated_at = timezone.now()
            location_model.save()
            return self._model_to_entity(location_model)
        except LocationModel.DoesNotExist:
            return None

    def soft_delete(self, location_id: str) -> bool:
        """Soft delete location"""
        try:
            location_model = LocationModel.objects.get(
                id=location_id, deleted_at__isnull=True
            )
            location_model.deleted_at = timezone.now()
            location_model.save()
            return True
        except LocationModel.DoesNotExist:
            return False

    def search_by_name(self, name: str) -> List[Location]:
        """Search locations by name (partial match)"""
        queryset = LocationModel.objects.filter(
            name__icontains=name, deleted_at__isnull=True
        )
        return [self._model_to_entity(location) for location in queryset]

    def get_rooms_by_location(self, location_id: str) -> List:
        """Get rooms for a location"""
        try:
            location_model = LocationModel.objects.get(
                id=location_id, deleted_at__isnull=True
            )

            from ...models import Room as RoomModel

            room_models = RoomModel.objects.filter(
                location=location_model, deleted_at__isnull=True
            )

            from ..repositories.django_room_repository import DjangoRoomRepository

            room_repo = DjangoRoomRepository()
            return [room_repo._model_to_entity(room) for room in room_models]
        except LocationModel.DoesNotExist:
            return []

    def has_active_rooms(self, location_id: str) -> bool:
        """Check if location has any active rooms"""
        from ...models import Room as RoomModel

        return RoomModel.objects.filter(
            location_id=location_id, deleted_at__isnull=True
        ).exists()

    def _model_to_entity(self, location_model: LocationModel) -> Location:
        """Convert Django model to domain entity"""
        return Location(
            id=str(location_model.id),
            name=location_model.name,
            address=location_model.address,
            description=location_model.description,
            created_at=location_model.created_at,
            updated_at=location_model.updated_at,
        )
