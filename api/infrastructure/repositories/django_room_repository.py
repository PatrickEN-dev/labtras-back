from typing import List, Optional, Dict, Any
from django.db import models
from django.utils import timezone

from ...models import (
    Room as RoomModel,
    Location as LocationModel,
    Booking as BookingModel,
)
from ...application.repositories.room_repository_interface import (
    RoomRepositoryInterface,
)
from ...domain.entities.room import Room


class DjangoRoomRepository(RoomRepositoryInterface):
    """
    Django ORM implementation of RoomRepositoryInterface
    """

    def create(self, data: Dict[str, Any]) -> Room:
        """Create a new room"""
        room_model = RoomModel.objects.create(**data)
        return self._model_to_entity(room_model)

    def get_by_id(self, room_id: str) -> Optional[Room]:
        """Get room by ID"""
        try:
            room_model = RoomModel.objects.select_related("location").get(
                id=room_id, deleted_at__isnull=True
            )
            return self._model_to_entity(room_model)
        except RoomModel.DoesNotExist:
            return None

    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Room]:
        """Get all rooms with optional filters"""
        queryset = RoomModel.objects.select_related("location").filter(
            deleted_at__isnull=True
        )

        if filters:
            if "location_id" in filters:
                queryset = queryset.filter(location_id=filters["location_id"])
            if "name" in filters:
                queryset = queryset.filter(name__icontains=filters["name"])
            if "capacity_min" in filters:
                queryset = queryset.filter(capacity__gte=filters["capacity_min"])
            if "capacity_max" in filters:
                queryset = queryset.filter(capacity__lte=filters["capacity_max"])

        return [self._model_to_entity(room) for room in queryset]

    def get_by_location(self, location_id: str) -> List[Room]:
        """Get rooms by location"""
        queryset = RoomModel.objects.select_related("location").filter(
            location_id=location_id, deleted_at__isnull=True
        )
        return [self._model_to_entity(room) for room in queryset]

    def get_available_rooms(
        self, start_date, end_date, location_id: Optional[str] = None
    ) -> List[Room]:
        """Get available rooms for a time period"""
        # Base queryset
        queryset = RoomModel.objects.select_related("location").filter(
            deleted_at__isnull=True
        )

        if location_id:
            queryset = queryset.filter(location_id=location_id)

        # Exclude rooms with conflicting bookings
        conflicting_bookings = BookingModel.objects.filter(
            start_date__lt=end_date, end_date__gt=start_date, deleted_at__isnull=True
        ).values_list("room_id", flat=True)

        queryset = queryset.exclude(id__in=conflicting_bookings)

        return [self._model_to_entity(room) for room in queryset]

    def update(self, room_id: str, data: Dict[str, Any]) -> Optional[Room]:
        """Update room"""
        try:
            room_model = RoomModel.objects.get(id=room_id, deleted_at__isnull=True)
            for key, value in data.items():
                setattr(room_model, key, value)
            room_model.updated_at = timezone.now()
            room_model.save()
            return self._model_to_entity(room_model)
        except RoomModel.DoesNotExist:
            return None

    def soft_delete(self, room_id: str) -> bool:
        """Soft delete room"""
        try:
            room_model = RoomModel.objects.get(id=room_id, deleted_at__isnull=True)
            room_model.deleted_at = timezone.now()
            room_model.save()
            return True
        except RoomModel.DoesNotExist:
            return False

    def check_name_uniqueness(
        self, name: str, location_id: str, exclude_room_id: Optional[str] = None
    ) -> bool:
        """Check if room name is unique within location"""
        queryset = RoomModel.objects.filter(
            name__iexact=name, location_id=location_id, deleted_at__isnull=True
        )

        if exclude_room_id:
            queryset = queryset.exclude(id=exclude_room_id)

        return not queryset.exists()

    def get_bookings_for_room(
        self, room_id: str, start_date=None, end_date=None
    ) -> List:
        """Get bookings for a room in a date range"""
        queryset = BookingModel.objects.filter(room_id=room_id, deleted_at__isnull=True)

        if start_date:
            queryset = queryset.filter(end_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_date__lte=end_date)

        # Convert to booking entities
        from ..repositories.django_booking_repository import DjangoBookingRepository

        booking_repo = DjangoBookingRepository()
        return [booking_repo._model_to_entity(booking) for booking in queryset]

    def get_available_rooms(
        self, start_date: Any, end_date: Any, location_id: Optional[str] = None
    ) -> List[Room]:
        """Get available rooms for a time period"""
        queryset = RoomModel.objects.filter(deleted_at__isnull=True)

        if location_id:
            queryset = queryset.filter(location_id=location_id)

        # Get rooms that don't have conflicting bookings
        conflicting_bookings = BookingModel.objects.filter(
            deleted_at__isnull=True, start_date__lt=end_date, end_date__gt=start_date
        ).values_list("room_id", flat=True)

        available_rooms = queryset.exclude(id__in=conflicting_bookings)

        return [self._model_to_entity(room) for room in available_rooms]

    def has_active_bookings(self, room_id: str) -> bool:
        """Check if room has any active bookings"""
        now = timezone.now()
        return BookingModel.objects.filter(
            room_id=room_id, deleted_at__isnull=True, end_date__gte=now
        ).exists()

    def get_room_bookings_count(self, room_id: str) -> Dict[str, int]:
        """Get booking statistics for a room"""
        now = timezone.now()

        total = BookingModel.objects.filter(
            room_id=room_id, deleted_at__isnull=True
        ).count()

        active = BookingModel.objects.filter(
            room_id=room_id,
            deleted_at__isnull=True,
            start_date__lte=now,
            end_date__gte=now,
        ).count()

        upcoming = BookingModel.objects.filter(
            room_id=room_id, deleted_at__isnull=True, start_date__gt=now
        ).count()

        completed = BookingModel.objects.filter(
            room_id=room_id, deleted_at__isnull=True, end_date__lt=now
        ).count()

        return {
            "total": total,
            "active": active,
            "upcoming": upcoming,
            "completed": completed,
        }

    def _model_to_entity(self, room_model: RoomModel) -> Room:
        """Convert Django model to domain entity"""
        return Room(
            id=str(room_model.id),
            name=room_model.name,
            capacity=room_model.capacity,
            location_id=str(room_model.location_id) if room_model.location_id else None,
            description=room_model.description,
            created_at=room_model.created_at,
            updated_at=room_model.updated_at,
            deleted_at=room_model.deleted_at,
        )
