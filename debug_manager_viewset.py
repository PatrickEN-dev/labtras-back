from rest_framework import viewsets, status
from rest_framework.response import Response

from ...application.use_cases.manager_use_cases import (
    CreateManagerUseCase,
)
from ...application.dto.manager_dto import ManagerInputDTO, ManagerOutputDTO
from ..repositories.django_manager_repository import DjangoManagerRepository
import traceback


class ManagerViewSetDebug(viewsets.ViewSet):
    """Debug version of Manager ViewSet"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_repository = DjangoManagerRepository()
        self.create_use_case = CreateManagerUseCase(self.manager_repository)

    def create(self, request):
        """Create a new manager with detailed debug"""
        try:
            print(f"DEBUG: Request data = {request.data}")

            # 1. Validate input using DTO
            input_dto = ManagerInputDTO(data=request.data)
            print(f"DEBUG: DTO created")

            if not input_dto.is_valid():
                print(f"DEBUG: DTO validation failed: {input_dto.errors}")
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            print(f"DEBUG: DTO validated data = {input_dto.validated_data}")

            manager = self.create_use_case.execute(input_dto.validated_data)
            print(f"DEBUG: Manager created = {manager}")

            output_dto = ManagerOutputDTO(manager)
            print(f"DEBUG: Output DTO created")

            result = output_dto.to_dict()
            print(f"DEBUG: Result = {result}")

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"DEBUG: Exception = {e}")
            traceback.print_exc()
            return Response(
                {
                    "error": "Internal server error",
                    "details": str(e),
                    "traceback": traceback.format_exc(),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
