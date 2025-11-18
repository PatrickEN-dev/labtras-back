from typing import List, Optional, Dict, Any
from django.db import models
from django.utils import timezone

from ...models import Manager as ManagerModel, Booking as BookingModel
from ...application.repositories.manager_repository_interface import (
    ManagerRepositoryInterface,
)
from ...domain.entities.manager import Manager


class DjangoManagerRepository(ManagerRepositoryInterface):
    """
    Django ORM implementation of ManagerRepositoryInterface
    """

    def create(self, data: Dict[str, Any]) -> Manager:
        """Create a new manager"""
        manager_model = ManagerModel.objects.create(**data)
        return self._model_to_entity(manager_model)

    def get_by_id(self, manager_id: str) -> Optional[Manager]:
        """Get manager by ID"""
        try:
            manager_model = ManagerModel.objects.get(
                id=manager_id, deleted_at__isnull=True
            )
            return self._model_to_entity(manager_model)
        except ManagerModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[Manager]:
        """Get manager by email"""
        try:
            manager_model = ManagerModel.objects.get(
                email__iexact=email, deleted_at__isnull=True
            )
            return self._model_to_entity(manager_model)
        except ManagerModel.DoesNotExist:
            return None

    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Manager]:
        """Get all managers with optional filters"""
        queryset = ManagerModel.objects.filter(deleted_at__isnull=True)

        if filters:
            if "name" in filters:
                queryset = queryset.filter(name__icontains=filters["name"])
            if "email" in filters:
                queryset = queryset.filter(email__icontains=filters["email"])

        return [self._model_to_entity(manager) for manager in queryset]

    def get_by_department(self, department: str) -> List[Manager]:
        """Get managers by department"""
        queryset = ManagerModel.objects.filter(
            department__iexact=department, deleted_at__isnull=True
        )
        return [self._model_to_entity(manager) for manager in queryset]

    def search_by_name(self, name: str) -> List[Manager]:
        """Search managers by name (partial match)"""
        queryset = ManagerModel.objects.filter(
            name__icontains=name, deleted_at__isnull=True
        )
        return [self._model_to_entity(manager) for manager in queryset]

    def update(self, manager_id: str, data: Dict[str, Any]) -> Optional[Manager]:
        """Update manager"""
        try:
            manager_model = ManagerModel.objects.get(
                id=manager_id, deleted_at__isnull=True
            )
            for key, value in data.items():
                setattr(manager_model, key, value)
            manager_model.updated_at = timezone.now()
            manager_model.save()
            return self._model_to_entity(manager_model)
        except ManagerModel.DoesNotExist:
            return None

    def soft_delete(self, manager_id: str) -> bool:
        """Soft delete manager"""
        try:
            manager_model = ManagerModel.objects.get(
                id=manager_id, deleted_at__isnull=True
            )
            manager_model.deleted_at = timezone.now()
            manager_model.save()
            return True
        except ManagerModel.DoesNotExist:
            return False

    def check_email_uniqueness(
        self, email: str, exclude_manager_id: Optional[str] = None
    ) -> bool:
        """Check if email is unique"""
        queryset = ManagerModel.objects.filter(
            email__iexact=email, deleted_at__isnull=True
        )

        if exclude_manager_id:
            queryset = queryset.exclude(id=exclude_manager_id)

        return not queryset.exists()

    def get_bookings_for_manager(self, manager_id: str) -> List:
        """Get bookings for a manager"""
        queryset = BookingModel.objects.filter(
            manager_id=manager_id, deleted_at__isnull=True
        )

        # Convert to booking entities
        from .django_booking_repository import DjangoBookingRepository

        booking_repo = DjangoBookingRepository()
        return [booking_repo._model_to_entity(booking) for booking in queryset]

    def get_active_bookings_count(self, manager_id: str) -> int:
        """Get count of active bookings for manager"""
        now = timezone.now()
        return BookingModel.objects.filter(
            manager_id=manager_id,
            start_date__lte=now,
            end_date__gte=now,
            deleted_at__isnull=True,
        ).count()

    def get_by_department(self, department: str) -> List[Manager]:
        """Get managers by department - Not implemented as department field doesn't exist"""
        # Department field doesn't exist in the model, returning empty list
        return []

    def search_by_name(self, name: str) -> List[Manager]:
        """Search managers by name (partial match)"""
        queryset = ManagerModel.objects.filter(
            name__icontains=name, deleted_at__isnull=True
        )
        return [self._model_to_entity(manager) for manager in queryset]

    def get_manager_bookings_count(self, manager_id: str) -> Dict[str, int]:
        """Get booking statistics for a manager"""
        now = timezone.now()

        total = BookingModel.objects.filter(
            manager_id=manager_id, deleted_at__isnull=True
        ).count()

        active = BookingModel.objects.filter(
            manager_id=manager_id,
            deleted_at__isnull=True,
            start_date__lte=now,
            end_date__gte=now,
        ).count()

        upcoming = BookingModel.objects.filter(
            manager_id=manager_id, deleted_at__isnull=True, start_date__gt=now
        ).count()

        completed = BookingModel.objects.filter(
            manager_id=manager_id, deleted_at__isnull=True, end_date__lt=now
        ).count()

        return {
            "total": total,
            "active": active,
            "upcoming": upcoming,
            "completed": completed,
        }

    def _model_to_entity(self, manager_model: ManagerModel) -> Manager:
        """Convert Django model to domain entity"""
        return Manager(
            id=str(manager_model.id),
            name=manager_model.name,
            email=manager_model.email,
            phone=manager_model.phone,
            created_at=manager_model.created_at,
            updated_at=manager_model.updated_at,
            deleted_at=manager_model.deleted_at,
        )
