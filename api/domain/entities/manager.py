from typing import Optional
from datetime import datetime
import uuid


class Manager:
    """
    Domain Entity: Manager
    Represents a person responsible for booking rooms
    """

    def __init__(
        self,
        id: str = None,
        name: str = None,
        email: str = None,
        phone: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __str__(self):
        return self.name or f"Manager {self.id}"

    @property
    def is_active(self) -> bool:
        """Domain method to check if manager is active"""
        return self.deleted_at is None

    def can_be_deleted(self, has_active_bookings: bool = False) -> bool:
        """Domain rule: Manager can only be deleted if they have no active bookings"""
        return not has_active_bookings

    def mark_as_deleted(self, deleted_at: datetime = None) -> None:
        """Domain method to soft delete manager"""
        self.deleted_at = deleted_at or datetime.now()

    def update_info(
        self, name: str = None, email: str = None, phone: str = None
    ) -> None:
        """Domain method to update manager information"""
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        self.updated_at = datetime.now()

    def validate_email_format(self) -> bool:
        """Domain rule: Validate email format"""
        if not self.email:
            return False
        import re

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, self.email))

    def validate_phone_format(self) -> bool:
        """Domain rule: Validate Brazilian phone format"""
        if not self.phone:
            return True  # Phone is optional
        import re

        # Brazilian phone pattern: (XX) 9XXXX-XXXX or similar variations
        phone_pattern = r"^\(?[1-9]{2}\)?\s?9?[0-9]{4,5}-?[0-9]{4}$"
        return bool(re.match(phone_pattern, self.phone.replace(" ", "")))
