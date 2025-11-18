from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ...application.use_cases.manager_use_cases import (
    CreateManagerUseCase,
    UpdateManagerUseCase,
    DeleteManagerUseCase,
    ListManagersUseCase,
    GetManagerUseCase,
    SearchManagersUseCase,
    GetManagerStatsUseCase,
)
from ...application.dto.manager_dto import ManagerInputDTO, ManagerOutputDTO
from ..repositories.django_manager_repository import DjangoManagerRepository


class ManagerViewSet(viewsets.ViewSet):
    """
    ViewSet for Manager operations using Clean Architecture

    This ViewSet handles HTTP requests and delegates business logic to Use Cases.
    No business rules are implemented here - only request/response handling.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_repository = DjangoManagerRepository()

        # Initialize use cases
        self.create_use_case = CreateManagerUseCase(self.manager_repository)
        self.update_use_case = UpdateManagerUseCase(self.manager_repository)
        self.delete_use_case = DeleteManagerUseCase(self.manager_repository)
        self.list_use_case = ListManagersUseCase(self.manager_repository)
        self.get_use_case = GetManagerUseCase(self.manager_repository)
        self.search_use_case = SearchManagersUseCase(self.manager_repository)
        self.stats_use_case = GetManagerStatsUseCase(self.manager_repository)

    def create(self, request):
        """Create a new manager"""
        try:

            input_dto = ManagerInputDTO(data=request.data)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            manager = self.create_use_case.execute(input_dto.validated_data)

            output_dto = ManagerOutputDTO(manager)
            return Response(output_dto.to_dict(), status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request):
        """List all managers"""
        try:
            filters = {}
            if request.query_params.get("department"):
                filters["department"] = request.query_params.get("department")
            if request.query_params.get("name"):
                filters["name"] = request.query_params.get("name")
            if request.query_params.get("email"):
                filters["email"] = request.query_params.get("email")

            if request.query_params.get("search"):
                filters["search"] = request.query_params.get("search")

            managers = self.list_use_case.execute(filters if filters else None)

            output_dtos = [ManagerOutputDTO(manager) for manager in managers]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """Get a specific manager"""
        try:
            manager = self.get_use_case.execute(pk)

            if not manager:
                return Response(
                    {"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
                )

            output_dto = ManagerOutputDTO(manager)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        """Update a manager"""
        try:
            input_dto = ManagerInputDTO(request.data, partial=True)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            manager = self.update_use_case.execute(pk, input_dto.validated_data)

            output_dto = ManagerOutputDTO(manager)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        """Partial update a manager"""
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """Delete a manager"""
        try:
            # 1. Execute use case
            success = self.delete_use_case.execute(pk)

            if success:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
                )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search managers by name"""
        try:
            name = request.query_params.get("name", "")

            if not name:
                return Response(
                    {"error": "name parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            managers = self.search_use_case.execute_by_name(name)

            output_dtos = [ManagerOutputDTO(manager) for manager in managers]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def by_department(self, request):
        """Get managers by department"""
        try:
            department = request.query_params.get("department")
            if not department:
                return Response(
                    {"error": "department parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            managers = self.list_use_case.execute_by_department(department)

            output_dtos = [ManagerOutputDTO(manager) for manager in managers]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def by_email(self, request):
        """Get manager by email"""
        try:
            email = request.query_params.get("email")
            if not email:
                return Response(
                    {"error": "email parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            manager = self.manager_repository.get_by_email(email)

            if not manager:
                return Response(
                    {"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
                )

            output_dto = ManagerOutputDTO(manager)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        """Get manager statistics"""
        try:

            stats = self.stats_use_case.execute(pk)

            return Response(stats, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
