from typing import List, Optional, Dict, Any

from ..repositories.manager_repository_interface import ManagerRepositoryInterface
from ...domain.services.manager_domain_service import ManagerDomainService
from ...domain.entities.manager import Manager


class CreateManagerUseCase:
    """
    Use Case: Create a new manager
    """

    def __init__(self, manager_repository: ManagerRepositoryInterface):
        self.manager_repository = manager_repository
        self.domain_service = ManagerDomainService()

    def execute(self, manager_data: Dict[str, Any]) -> Manager:
        """
        Execute the use case to create a manager
        """

        email = manager_data.get("email")
        name = manager_data.get("name")

        ManagerDomainService.validate_email_format(email)
        ManagerDomainService.validate_name_format(name)

        # 3. Check email uniqueness
        if not ManagerDomainService.validate_email_uniqueness(email):
            raise ValueError(f"Manager with email '{email}' already exists")

        # 4. Prepare data for repository
        repository_data = {
            "name": name,
            "email": email,
            "phone": manager_data.get("phone"),
        }

        if repository_data["phone"]:
            ManagerDomainService.validate_phone_format(repository_data["phone"])

        return self.manager_repository.create(repository_data)


class UpdateManagerUseCase:
    """
    Use Case: Update an existing manager
    """

    def __init__(self, manager_repository: ManagerRepositoryInterface):
        self.manager_repository = manager_repository
        self.domain_service = ManagerDomainService()

    def execute(self, manager_id: str, update_data: Dict[str, Any]) -> Manager:
        """
        Execute the use case to update a manager
        """
        # 1. Get existing manager
        existing_manager = self.manager_repository.get_by_id(manager_id)
        if not existing_manager:
            raise ValueError("Manager not found")

        # 2. Validate updates
        from ...domain.services.manager_domain_service import ManagerDomainService

        if "email" in update_data:
            new_email = update_data["email"]
            ManagerDomainService.validate_email_format(new_email)

            # Check uniqueness only if email is being changed
            if new_email != existing_manager.email:
                if not ManagerDomainService.validate_email_uniqueness(
                    new_email, manager_id
                ):
                    raise ValueError(f"Manager with email '{new_email}' already exists")

        if "name" in update_data:
            ManagerDomainService.validate_name_format(update_data["name"])

        if "phone" in update_data and update_data["phone"]:
            ManagerDomainService.validate_phone_format(update_data["phone"])

        if "department" in update_data and update_data["department"]:
            ManagerDomainService.validate_department_format(update_data["department"])

        # 3. Update manager
        updated_manager = self.manager_repository.update(manager_id, update_data)
        if not updated_manager:
            raise ValueError("Failed to update manager")

        return updated_manager


class DeleteManagerUseCase:
    """
    Use Case: Delete a manager (soft delete)
    """

    def __init__(self, manager_repository: ManagerRepositoryInterface):
        self.manager_repository = manager_repository
        self.domain_service = ManagerDomainService()

    def execute(self, manager_id: str) -> bool:
        """
        Execute the use case to delete a manager
        """
        # 1. Get existing manager
        existing_manager = self.manager_repository.get_by_id(manager_id)
        if not existing_manager:
            raise ValueError("Manager not found")

        # 2. Check if manager has active bookings
        if ManagerDomainService.has_active_bookings(existing_manager):
            raise ValueError("Cannot delete manager with active bookings")

        # 3. Delete manager
        return self.manager_repository.soft_delete(manager_id)


class ListManagersUseCase:
    """
    Use Case: List managers with optional filters
    """

    def __init__(self, manager_repository: ManagerRepositoryInterface):
        self.manager_repository = manager_repository

    def execute(self, filters: Optional[Dict[str, Any]] = None) -> List[Manager]:
        """
        Execute the use case to list managers
        """
        return self.manager_repository.get_all(filters)

    def execute_by_department(self, department: str) -> List[Manager]:
        """
        Get managers by department
        """
        return self.manager_repository.get_by_department(department)


class GetManagerUseCase:
    """
    Use Case: Get a single manager by ID
    """

    def __init__(self, manager_repository: ManagerRepositoryInterface):
        self.manager_repository = manager_repository

    def execute(self, manager_id: str) -> Optional[Manager]:
        """
        Execute the use case to get a manager
        """
        return self.manager_repository.get_by_id(manager_id)


class SearchManagersUseCase:
    """
    Use Case: Search managers by various criteria
    """

    def __init__(self, manager_repository: ManagerRepositoryInterface):
        self.manager_repository = manager_repository

    def execute_by_name(self, name: str) -> List[Manager]:
        """
        Search managers by name (partial match)
        """
        return self.manager_repository.search_by_name(name)

    def execute_by_email(self, email: str) -> Optional[Manager]:
        """
        Find manager by exact email
        """
        return self.manager_repository.get_by_email(email)


class GetManagerStatsUseCase:
    """
    Use Case: Get manager statistics (bookings count, etc.)
    """

    def __init__(self, manager_repository: ManagerRepositoryInterface):
        self.manager_repository = manager_repository

    def execute(self, manager_id: str) -> Dict[str, Any]:
        """
        Execute the use case to get manager statistics
        """
        # 1. Get manager
        manager = self.manager_repository.get_by_id(manager_id)
        if not manager:
            raise ValueError("Manager not found")

        # 2. Get statistics from domain service
        stats = ManagerDomainService.calculate_manager_stats(manager)

        return {
            "manager_id": manager_id,
            "manager_name": manager.name,
            "total_bookings": stats.get("total_bookings", 0),
            "active_bookings": stats.get("active_bookings", 0),
            "completed_bookings": stats.get("completed_bookings", 0),
            "cancelled_bookings": stats.get("cancelled_bookings", 0),
        }
