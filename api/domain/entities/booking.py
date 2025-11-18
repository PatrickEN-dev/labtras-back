from typing import Optional
from datetime import datetime
import uuid


class Booking:
    """
    Domain Entity: Booking
    Represents a room reservation with business rules
    """

    def __init__(
        self,
        id: str = None,
        room_id: str = None,
        manager_id: str = None,
        room=None,
        manager=None,
        name: str = None,
        description: Optional[str] = None,
        start_date: datetime = None,
        end_date: datetime = None,
        coffee_option: bool = False,
        coffee_quantity: Optional[int] = None,
        coffee_description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.room_id = room_id
        self.manager_id = manager_id
        self.room = room
        self.manager = manager
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.coffee_option = coffee_option
        self.coffee_quantity = coffee_quantity
        self.coffee_description = coffee_description
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        if self.name:
            return f"Booking {self.name} ({self.id[:8]}...)"
        return f"Booking {self.id} - {self.start_date} to {self.end_date}"

    @property
    def is_active(self) -> bool:
        """Domain method to check if booking is active"""
        return self.deleted_at is None

    @property
    def is_current(self) -> bool:
        """Domain method to check if booking is currently happening"""
        now = datetime.now()
        return self.start_date <= now <= self.end_date and self.is_active

    @property
    def is_future(self) -> bool:
        """Domain method to check if booking is in the future"""
        return self.start_date > datetime.now() and self.is_active

    @property
    def duration_hours(self) -> float:
        """Domain method to calculate booking duration in hours"""
        if self.start_date and self.end_date:
            duration = self.end_date - self.start_date
            return duration.total_seconds() / 3600
        return 0

    def validate_dates(self):
        """Domain rule: Start date must be before end date"""
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValueError("Start date must be before end date")

    def validate_coffee_rules(self):
        """Domain rule: If coffee is requested, quantity must be provided"""
        if self.coffee_option and not self.coffee_quantity:
            raise ValueError(
                "Coffee quantity is required when coffee option is selected"
            )

        if not self.coffee_option:
            self.coffee_quantity = None
            self.coffee_description = None

    def can_be_modified(self) -> bool:
        """Domain rule: Booking can only be modified if it's in the future"""
        return self.is_future

    def can_be_cancelled(self) -> bool:
        """Domain rule: Booking can be cancelled if it's not yet finished"""
        return self.end_date > datetime.now() and self.is_active

    def mark_as_deleted(self, deleted_at: datetime = None) -> None:
        """Domain method to soft delete booking"""
        self.deleted_at = deleted_at or datetime.now()

    def update_booking(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        coffee_option: bool = None,
        coffee_quantity: int = None,
        coffee_description: str = None,
    ) -> None:
        """Domain method to update booking information"""
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if coffee_option is not None:
            self.coffee_option = coffee_option
        if coffee_quantity is not None:
            self.coffee_quantity = coffee_quantity
        if coffee_description is not None:
            self.coffee_description = coffee_description

        self.updated_at = datetime.now()

        # Validate after updating
        self.validate_dates()
        self.validate_coffee_rules()
