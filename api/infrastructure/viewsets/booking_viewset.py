from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ...application.use_cases.booking_use_cases import (
    CreateBookingUseCase,
    UpdateBookingUseCase,
    CancelBookingUseCase,
    ListBookingsUseCase,
    GetBookingUseCase,
)
from ...application.dto.booking_dto import BookingInputDTO, BookingOutputDTO
from ..repositories.django_booking_repository import DjangoBookingRepository
from ..repositories.django_room_repository import DjangoRoomRepository
from ..repositories.django_manager_repository import DjangoManagerRepository


class BookingViewSet(viewsets.ViewSet):
    """
    ViewSet for Booking operations using Clean Architecture

    This ViewSet handles HTTP requests and delegates business logic to Use Cases.
    No business rules are implemented here - only request/response handling.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.booking_repository = DjangoBookingRepository()
        self.room_repository = DjangoRoomRepository()
        self.manager_repository = DjangoManagerRepository()

        self.create_use_case = CreateBookingUseCase(
            self.booking_repository, self.room_repository, self.manager_repository
        )
        self.update_use_case = UpdateBookingUseCase(
            self.booking_repository, self.room_repository, self.manager_repository
        )
        self.cancel_use_case = CancelBookingUseCase(self.booking_repository)
        self.list_use_case = ListBookingsUseCase(self.booking_repository)
        self.get_use_case = GetBookingUseCase(self.booking_repository)

    def create(self, request):
        """Create a new booking"""
        try:

            input_dto = BookingInputDTO(request.data)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            booking = self.create_use_case.execute(input_dto.validated_data)

            output_dto = BookingOutputDTO(booking)
            return Response(output_dto.to_dict(), status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request):
        """List all bookings"""
        try:

            filters = {}
            # Aceitar tanto 'room' quanto 'room_id' para compatibilidade
            if request.query_params.get("room") or request.query_params.get("room_id"):
                filters["room_id"] = request.query_params.get(
                    "room"
                ) or request.query_params.get("room_id")

            # Aceitar tanto 'manager' quanto 'manager_id' para compatibilidade
            if request.query_params.get("manager") or request.query_params.get(
                "manager_id"
            ):
                filters["manager_id"] = request.query_params.get(
                    "manager"
                ) or request.query_params.get("manager_id")

            # Aceitar diferentes formatos de datas
            if request.query_params.get("start_date_from") or request.query_params.get(
                "start_date"
            ):
                filters["start_date_from"] = request.query_params.get(
                    "start_date_from"
                ) or request.query_params.get("start_date")

            if request.query_params.get("start_date_to") or request.query_params.get(
                "end_date"
            ):
                filters["start_date_to"] = request.query_params.get(
                    "start_date_to"
                ) or request.query_params.get("end_date")

            if request.query_params.get("coffee_option"):
                filters["coffee_option"] = (
                    request.query_params.get("coffee_option").lower() == "true"
                )

            bookings = self.list_use_case.execute(filters if filters else None)

            output_dtos = [BookingOutputDTO(booking) for booking in bookings]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """Get a specific booking"""
        try:
            # 1. Execute use case
            booking = self.get_use_case.execute(pk)

            if not booking:
                return Response(
                    {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
                )

            output_dto = BookingOutputDTO(booking)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        """Update a booking"""
        try:

            input_dto = BookingInputDTO(request.data, partial=True)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            booking = self.update_use_case.execute(pk, input_dto.validated_data)

            output_dto = BookingOutputDTO(booking)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        """Partial update a booking"""
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """Cancel (soft delete) a booking"""
        try:
            # 1. Execute use case
            success = self.cancel_use_case.execute(pk)

            if success:
                return Response(
                    {"message": "Booking cancelled successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
                )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def by_room(self, request):
        """Get bookings by room"""
        try:
            room_id = request.query_params.get("room_id")
            if not room_id:
                return Response(
                    {"error": "room_id parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            bookings = self.list_use_case.execute_by_room(room_id)

            output_dtos = [BookingOutputDTO(booking) for booking in bookings]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def by_manager(self, request):
        """Get bookings by manager"""
        try:
            manager_id = request.query_params.get("manager_id")
            if not manager_id:
                return Response(
                    {"error": "manager_id parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            bookings = self.list_use_case.execute_by_manager(manager_id)

            output_dtos = [BookingOutputDTO(booking) for booking in bookings]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
