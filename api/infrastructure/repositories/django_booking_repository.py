from typing import List, Optional, Dict, Any
from django.db import models
from django.utils import timezone

from ...models import (
    Booking as BookingModel,
    Room as RoomModel,
    Manager as ManagerModel,
)
from ...application.repositories.booking_repository_interface import (
    BookingRepositoryInterface,
)
from ...domain.entities.booking import Booking


class DjangoBookingRepository(BookingRepositoryInterface):
    """
    Django ORM implementation of BookingRepositoryInterface
    """

    def create(self, data: Dict[str, Any]) -> Booking:
        """Create a new booking"""
        booking_model = BookingModel.objects.create(**data)
        # Reload with related data
        booking_model = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).get(id=booking_model.id)
        return self._model_to_entity(booking_model)

    def get_by_id(self, booking_id: str) -> Optional[Booking]:
        """Get booking by ID"""
        try:
            booking_model = BookingModel.objects.select_related(
                "room", "manager", "room__location"
            ).get(id=booking_id, deleted_at__isnull=True)
            return self._model_to_entity(booking_model)
        except BookingModel.DoesNotExist:
            return None

    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Booking]:
        """Get all bookings with optional filters"""
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(deleted_at__isnull=True)

        if filters:
            if "room_id" in filters:
                queryset = queryset.filter(room_id=filters["room_id"])
            if "manager_id" in filters:
                queryset = queryset.filter(manager_id=filters["manager_id"])
            if "start_date_from" in filters:
                queryset = queryset.filter(start_date__gte=filters["start_date_from"])
            if "start_date_to" in filters:
                queryset = queryset.filter(start_date__lte=filters["start_date_to"])
            if "end_date_from" in filters:
                queryset = queryset.filter(end_date__gte=filters["end_date_from"])
            if "end_date_to" in filters:
                queryset = queryset.filter(end_date__lte=filters["end_date_to"])
            if "coffee_option" in filters:
                queryset = queryset.filter(coffee_option=filters["coffee_option"])

        return [self._model_to_entity(booking) for booking in queryset]

    def get_by_room(self, room_id: str) -> List[Booking]:
        """Get bookings by room"""
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(room_id=room_id, deleted_at__isnull=True)
        return [self._model_to_entity(booking) for booking in queryset]

    def get_by_manager(self, manager_id: str) -> List[Booking]:
        """Get bookings by manager"""
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(manager_id=manager_id, deleted_at__isnull=True)
        return [self._model_to_entity(booking) for booking in queryset]

    def get_conflicting_bookings(
        self,
        room_id: str,
        start_date,
        end_date,
        exclude_booking_id: Optional[str] = None,
    ) -> List[Booking]:
        """Get bookings that conflict with the given time range"""
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(
            room_id=room_id,
            start_date__lt=end_date,
            end_date__gt=start_date,
            deleted_at__isnull=True,
        )

        if exclude_booking_id:
            queryset = queryset.exclude(id=exclude_booking_id)

        return [self._model_to_entity(booking) for booking in queryset]

    def update(self, booking_id: str, data: Dict[str, Any]) -> Optional[Booking]:
        """Update booking"""
        try:
            booking_model = BookingModel.objects.get(
                id=booking_id, deleted_at__isnull=True
            )
            for key, value in data.items():
                setattr(booking_model, key, value)
            booking_model.updated_at = timezone.now()
            booking_model.save()
            return self._model_to_entity(booking_model)
        except BookingModel.DoesNotExist:
            return None

    def soft_delete(self, booking_id: str) -> bool:
        """Soft delete booking"""
        try:
            booking_model = BookingModel.objects.get(
                id=booking_id, deleted_at__isnull=True
            )
            booking_model.deleted_at = timezone.now()
            booking_model.save()
            return True
        except BookingModel.DoesNotExist:
            return False

    def get_bookings_in_date_range(self, start_date, end_date) -> List[Booking]:
        """Get all bookings in a date range"""
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(
            start_date__lt=end_date, end_date__gt=start_date, deleted_at__isnull=True
        )
        return [self._model_to_entity(booking) for booking in queryset]

    def get_active_bookings(self, current_time=None) -> List[Booking]:
        """Get currently active bookings"""
        if current_time is None:
            current_time = timezone.now()

        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(
            start_date__lte=current_time,
            end_date__gte=current_time,
            deleted_at__isnull=True,
        )
        return [self._model_to_entity(booking) for booking in queryset]

    def find_conflicts(
        self,
        room_id: str,
        start_date,
        end_date,
        exclude_booking_id: Optional[str] = None,
    ) -> List[Booking]:
        """Find conflicting bookings for a time period"""
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(
            room_id=room_id,
            start_date__lt=end_date,
            end_date__gt=start_date,
            deleted_at__isnull=True,
        )

        if exclude_booking_id:
            queryset = queryset.exclude(id=exclude_booking_id)

        return [self._model_to_entity(booking) for booking in queryset]

    def get_active_bookings(
        self, manager_id: Optional[str] = None, room_id: Optional[str] = None
    ) -> List[Booking]:
        """Get currently active bookings"""
        now = timezone.now()
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(deleted_at__isnull=True, start_date__lte=now, end_date__gte=now)

        if manager_id:
            queryset = queryset.filter(manager_id=manager_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)

        return [self._model_to_entity(booking) for booking in queryset]

    def get_upcoming_bookings(
        self, manager_id: Optional[str] = None, room_id: Optional[str] = None
    ) -> List[Booking]:
        """Get upcoming bookings"""
        now = timezone.now()
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(deleted_at__isnull=True, start_date__gt=now)

        if manager_id:
            queryset = queryset.filter(manager_id=manager_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)

        return [self._model_to_entity(booking) for booking in queryset]

    def get_bookings_by_date_range(
        self,
        start_date,
        end_date,
        manager_id: Optional[str] = None,
        room_id: Optional[str] = None,
    ) -> List[Booking]:
        """Get bookings within a date range"""
        queryset = BookingModel.objects.select_related(
            "room", "manager", "room__location"
        ).filter(
            deleted_at__isnull=True, start_date__lte=end_date, end_date__gte=start_date
        )

        if manager_id:
            queryset = queryset.filter(manager_id=manager_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)

        return [self._model_to_entity(booking) for booking in queryset]

    def can_manager_book_room(
        self, manager_id: str, room_id: str, start_date, end_date
    ) -> bool:
        """Check if manager can book the room for given time period"""

        conflicts = self.find_conflicts(room_id, start_date, end_date)
        return len(conflicts) == 0

    def _model_to_entity(self, booking_model: BookingModel) -> Booking:
        """Convert Django model to domain entity"""
        from ...domain.entities.room import Room
        from ...domain.entities.manager import Manager

        # Convert related objects to entities if they exist
        room_entity = None
        if hasattr(booking_model, "room") and booking_model.room:
            room_entity = Room(
                id=str(booking_model.room.id),
                name=booking_model.room.name,
                capacity=booking_model.room.capacity,
                location_id=(
                    str(booking_model.room.location_id)
                    if booking_model.room.location_id
                    else None
                ),
            )

        manager_entity = None
        if hasattr(booking_model, "manager") and booking_model.manager:
            manager_entity = Manager(
                id=str(booking_model.manager.id),
                name=booking_model.manager.name,
                email=booking_model.manager.email,
            )

        return Booking(
            id=str(booking_model.id),
            room_id=str(booking_model.room_id) if booking_model.room_id else None,
            manager_id=(
                str(booking_model.manager_id) if booking_model.manager_id else None
            ),
            room=room_entity,
            manager=manager_entity,
            name=booking_model.name,
            description=booking_model.description,
            start_date=booking_model.start_date,
            end_date=booking_model.end_date,
            coffee_option=booking_model.coffee_option,
            coffee_quantity=booking_model.coffee_quantity,
            coffee_description=booking_model.coffee_description,
            created_at=booking_model.created_at,
            updated_at=booking_model.updated_at,
            deleted_at=booking_model.deleted_at,
        )
