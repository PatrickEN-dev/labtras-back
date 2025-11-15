from typing import Optional
from datetime import datetime, timedelta
from django.utils import timezone


class BookingDomainService:
    """
    Domain Service for complex booking business rules
    that involve multiple entities or external concerns
    """

    @staticmethod
    def validate_booking_time_rules(start_date: datetime, end_date: datetime) -> None:
        """
        Domain rule: Validate booking time constraints
        """
        if not start_date or not end_date:
            raise ValueError("Start date and end date are required")

        if start_date >= end_date:
            raise ValueError("Start date must be before end date")

        now = timezone.now()
        if start_date < now - timedelta(minutes=5):
            raise ValueError("Cannot create booking in the past")

        duration = end_date - start_date
        if duration > timedelta(hours=8):
            raise ValueError("Booking duration cannot exceed 8 hours")

        if duration < timedelta(minutes=30):
            raise ValueError("Booking duration must be at least 30 minutes")

    @staticmethod
    def validate_coffee_requirements(
        coffee_option: bool, coffee_quantity: Optional[int]
    ) -> None:
        """
        Domain rule: Validate coffee service requirements
        """
        if coffee_option:
            if not coffee_quantity or coffee_quantity <= 0:
                raise ValueError(
                    "Coffee quantity must be specified when coffee option is enabled"
                )

            if coffee_quantity > 50:
                raise ValueError(
                    "Coffee quantity cannot exceed 50 servings per booking"
                )
        else:
            if coffee_quantity and coffee_quantity > 0:
                raise ValueError(
                    "Coffee quantity should not be specified when coffee option is disabled"
                )

    @staticmethod
    def can_modify_booking(booking) -> bool:
        """
        Domain rule: Check if a booking can be modified
        """

        now = timezone.now()
        return booking.start_date > now

    @staticmethod
    def can_cancel_booking(booking) -> bool:
        """
        Domain rule: Check if a booking can be cancelled
        """

        now = timezone.now()
        return booking.end_date > now

    @staticmethod
    def calculate_booking_duration_hours(
        start_date: datetime, end_date: datetime
    ) -> float:
        """
        Domain rule: Calculate booking duration in hours
        """
        duration = end_date - start_date
        return duration.total_seconds() / 3600

    @staticmethod
    def is_weekend_booking(start_date: datetime) -> bool:
        """
        Domain rule: Check if booking is on weekend
        """
        return start_date.weekday() >= 5  # Saturday = 5, Sunday = 6

    @staticmethod
    def is_business_hours(start_date: datetime, end_date: datetime) -> bool:
        """
        Domain rule: Check if booking is within business hours (9 AM - 6 PM)
        """
        business_start = 9  # 9 AM
        business_end = 18  # 6 PM

        start_hour = start_date.hour
        end_hour = end_date.hour

        return (
            business_start <= start_hour < business_end
            and business_start < end_hour <= business_end
        )
