from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from ...application.use_cases.room_use_cases import (
    CreateRoomUseCase,
    UpdateRoomUseCase,
    DeleteRoomUseCase,
    ListRoomsUseCase,
    GetRoomUseCase,
    CheckRoomAvailabilityUseCase,
)
from ...application.dto.room_dto import RoomInputDTO, RoomOutputDTO
from ..repositories.django_room_repository import DjangoRoomRepository
from ..repositories.django_location_repository import DjangoLocationRepository


class RoomViewSet(viewsets.ViewSet):
    """
    ViewSet for Room operations using Clean Architecture

    This ViewSet handles HTTP requests and delegates business logic to Use Cases.
    No business rules are implemented here - only request/response handling.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_repository = DjangoRoomRepository()
        self.location_repository = DjangoLocationRepository()

        # Initialize use cases
        self.create_use_case = CreateRoomUseCase(
            self.room_repository, self.location_repository
        )
        self.update_use_case = UpdateRoomUseCase(
            self.room_repository, self.location_repository
        )
        self.delete_use_case = DeleteRoomUseCase(self.room_repository)
        self.list_use_case = ListRoomsUseCase(self.room_repository)
        self.get_use_case = GetRoomUseCase(self.room_repository)
        self.availability_use_case = CheckRoomAvailabilityUseCase(self.room_repository)

    def create(self, request):
        """Create a new room"""
        try:
            # 1. Validate input using DTO
            input_dto = RoomInputDTO(request.data)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Execute use case
            room = self.create_use_case.execute(input_dto.validated_data)

            # 3. Return response using DTO
            output_dto = RoomOutputDTO(room)
            return Response(output_dto.to_dict(), status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request):
        """List all rooms"""
        try:
            # 1. Extract filters from query parameters
            filters = {}

            if request.query_params.get("location") or request.query_params.get(
                "location_id"
            ):
                filters["location_id"] = request.query_params.get(
                    "location"
                ) or request.query_params.get("location_id")
            if request.query_params.get("name"):
                filters["name"] = request.query_params.get("name")
            if request.query_params.get("capacity_min"):
                try:
                    filters["capacity_min"] = int(
                        request.query_params.get("capacity_min")
                    )
                except ValueError:
                    pass
            if request.query_params.get("capacity_max"):
                try:
                    filters["capacity_max"] = int(
                        request.query_params.get("capacity_max")
                    )
                except ValueError:
                    pass

            # 2. Execute use case
            rooms = self.list_use_case.execute(filters if filters else None)

            # 3. Return response using DTOs
            output_dtos = [RoomOutputDTO(room) for room in rooms]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """Get a specific room"""
        try:
            room = self.get_use_case.execute(pk)

            if not room:
                return Response(
                    {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
                )

            output_dto = RoomOutputDTO(room)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        """Update a room"""
        try:
            input_dto = RoomInputDTO(request.data, partial=True)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            room = self.update_use_case.execute(pk, input_dto.validated_data)

            output_dto = RoomOutputDTO(room)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        """Partial update a room"""
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """Delete a room"""
        try:
            success = self.delete_use_case.execute(pk)

            if success:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
                )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def by_location(self, request):
        """Get rooms by location"""
        try:
            location_id = request.query_params.get("location_id")
            if not location_id:
                return Response(
                    {"error": "location_id parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            rooms = self.list_use_case.execute_by_location(location_id)

            output_dtos = [RoomOutputDTO(room) for room in rooms]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def available(self, request):
        """Get available rooms for a time period"""
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            location_id = request.query_params.get("location_id")

            if not start_date or not end_date:
                return Response(
                    {"error": "start_date and end_date parameters are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            rooms = self.list_use_case.execute_available_rooms(
                start_date, end_date, location_id
            )

            output_dtos = [RoomOutputDTO(room) for room in rooms]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def check_availability(self, request, pk=None):
        """Check if a room is available for booking"""
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            if not start_date or not end_date:
                return Response(
                    {"error": "start_date and end_date parameters are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            result = self.availability_use_case.execute(pk, start_date, end_date)

            return Response(result, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
