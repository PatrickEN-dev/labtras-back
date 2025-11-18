from typing import Dict, Any, Optional
import re
from django.utils import timezone


class ManagerDomainService:
    """
    Domain service for manager-related business logic
    """

    @staticmethod
    def validate_email_format(email: str) -> None:
        """
        Validate email format using regex
        """
        if not email or not email.strip():
            raise ValueError("Email is required")

        email = email.strip()
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_name_format(name: str) -> None:
        """
        Validate name format
        """
        if not name or not name.strip():
            raise ValueError("Name is required")

        name = name.strip()
        if len(name) < 2:
            raise ValueError("Name must have at least 2 characters")

        if len(name) > 100:
            raise ValueError("Name cannot exceed 100 characters")

    @staticmethod
    def validate_phone_format(phone: str) -> None:
        """
        Validate phone format (Brazilian format)
        """
        if not phone or not phone.strip():
            return

        phone = phone.strip()
        clean_phone = re.sub(r"[\s\-\(\)\+]", "", phone)

        # Brazilian phone patterns
        if not re.match(r"^(\+55)?\d{10,11}$", clean_phone):
            raise ValueError(
                "Invalid phone format. Use Brazilian format: +55 11 99999-9999"
            )

    @staticmethod
    def validate_email_uniqueness(email: str, exclude_id: Optional[str] = None) -> bool:
        """
        Validate email uniqueness by checking with repository
        This should be implemented with actual database check via repository
        """

        from ...infrastructure.repositories.django_manager_repository import (
            DjangoManagerRepository,
        )

        repository = DjangoManagerRepository()
        return repository.check_email_uniqueness(email, exclude_id)

    @staticmethod
    def has_active_bookings(manager) -> bool:
        """
        Check if manager has active bookings
        """

        from ...infrastructure.repositories.django_manager_repository import (
            DjangoManagerRepository,
        )

        repository = DjangoManagerRepository()
        active_count = repository.get_active_bookings_count(manager.id)
        return active_count > 0

    @staticmethod
    def calculate_manager_stats(manager) -> Dict[str, Any]:
        """
        Calculate manager statistics
        """

        from ...infrastructure.repositories.django_manager_repository import (
            DjangoManagerRepository,
        )

        repository = DjangoManagerRepository()
        bookings = repository.get_bookings_for_manager(manager.id)

        now = timezone.now()
        stats = {
            "total_bookings": len(bookings),
            "active_bookings": 0,
            "completed_bookings": 0,
            "cancelled_bookings": 0,
            "future_bookings": 0,
            "past_bookings": 0,
        }

        for booking in bookings:
            # Check if booking is active (currently happening)
            if booking.start_date <= now <= booking.end_date:
                stats["active_bookings"] += 1
            elif booking.end_date < now:
                stats["completed_bookings"] += 1
            elif booking.start_date > now:
                stats["future_bookings"] += 1

            # Note: cancelled_bookings would require a status field in the booking
            # For now, we're using soft delete, so cancelled bookings won't appear here

        stats["past_bookings"] = stats["completed_bookings"]

        return stats

    @staticmethod
    def validate_department_format(department: str) -> None:
        """
        Validate department format
        """
        if department and department.strip():
            department = department.strip()
            if len(department) > 50:
                raise ValueError("Department name cannot exceed 50 characters")
