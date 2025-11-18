from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ...domain.entities.manager import Manager


class ManagerRepositoryInterface(ABC):
    """
    Repository interface for Manager entity
    """

    @abstractmethod
    def get_by_id(self, manager_id: str) -> Optional[Manager]:
        """Get a manager by its ID"""
        pass

    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Manager]:
        """Get all managers with optional filters"""
        pass

    @abstractmethod
    def create(self, manager_data: Dict[str, Any]) -> Manager:
        """Create a new manager"""
        pass

    @abstractmethod
    def update(
        self, manager_id: str, manager_data: Dict[str, Any]
    ) -> Optional[Manager]:
        """Update an existing manager"""
        pass

    @abstractmethod
    def soft_delete(self, manager_id: str) -> bool:
        """Soft delete a manager"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Manager]:
        """Get manager by email"""
        pass

    @abstractmethod
    def get_by_department(self, department: str) -> List[Manager]:
        """Get managers by department"""
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Manager]:
        """Search managers by name (partial match)"""
        pass

    @abstractmethod
    def get_manager_bookings_count(self, manager_id: str) -> Dict[str, int]:
        """Get booking statistics for a manager"""
        pass
