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

    def _model_to_entity(self, booking_model: BookingModel) -> Booking:
        """Convert Django model to domain entity"""
        # Import here to avoid circular imports
        from ..repositories.django_room_repository import DjangoRoomRepository
        from ..repositories.django_manager_repository import DjangoManagerRepository

        room_repo = DjangoRoomRepository()
        manager_repo = DjangoManagerRepository()

        room_entity = (
            room_repo._model_to_entity(booking_model.room)
            if booking_model.room
            else None
        )
        manager_entity = (
            manager_repo._model_to_entity(booking_model.manager)
            if booking_model.manager
            else None
        )

        return Booking(
            id=str(booking_model.id),
            room=room_entity,
            room_id=str(booking_model.room_id) if booking_model.room_id else None,
            manager=manager_entity,
            manager_id=(
                str(booking_model.manager_id) if booking_model.manager_id else None
            ),
            start_date=booking_model.start_date,
            end_date=booking_model.end_date,
            coffee_option=booking_model.coffee_option,
            coffee_quantity=booking_model.coffee_quantity,
            coffee_description=booking_model.coffee_description,
            created_at=booking_model.created_at,
            updated_at=booking_model.updated_at,
        )
