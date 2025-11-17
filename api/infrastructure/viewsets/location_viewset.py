from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from ...application.use_cases.location_use_cases import (
    CreateLocationUseCase,
    UpdateLocationUseCase,
    DeleteLocationUseCase,
    ListLocationsUseCase,
    GetLocationUseCase,
    SearchLocationsUseCase,
    GetLocationWithRoomsUseCase,
)
from ...application.dto.location_dto import LocationInputDTO, LocationOutputDTO
from ..repositories.django_location_repository import DjangoLocationRepository


class LocationViewSet(viewsets.ViewSet):
    """
    ViewSet for Location operations using Clean Architecture

    This ViewSet handles HTTP requests and delegates business logic to Use Cases.
    No business rules are implemented here - only request/response handling.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_repository = DjangoLocationRepository()

        # Initialize use cases
        self.create_use_case = CreateLocationUseCase(self.location_repository)
        self.update_use_case = UpdateLocationUseCase(self.location_repository)
        self.delete_use_case = DeleteLocationUseCase(self.location_repository)
        self.list_use_case = ListLocationsUseCase(self.location_repository)
        self.get_use_case = GetLocationUseCase(self.location_repository)
        self.search_use_case = SearchLocationsUseCase(self.location_repository)
        self.get_with_rooms_use_case = GetLocationWithRoomsUseCase(
            self.location_repository
        )

    def create(self, request):
        """Create a new location"""
        try:
            input_dto = LocationInputDTO(request.data)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            location = self.create_use_case.execute(input_dto.validated_data)

            output_dto = LocationOutputDTO(location)
            return Response(output_dto.to_dict(), status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request):
        """List all locations"""
        try:

            filters = {}
            if request.query_params.get("name"):
                filters["name"] = request.query_params.get("name")
            if request.query_params.get("address"):
                filters["address"] = request.query_params.get("address")

            if request.query_params.get("search"):
                filters["search"] = request.query_params.get("search")

            locations = self.list_use_case.execute(filters if filters else None)

            output_dtos = [LocationOutputDTO(location) for location in locations]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """Get a specific location"""
        try:
            location = self.get_use_case.execute(pk)

            if not location:
                return Response(
                    {"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # 2. Return response using DTO
            output_dto = LocationOutputDTO(location)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        """Update a location"""
        try:
            input_dto = LocationInputDTO(request.data, partial=True)
            if not input_dto.is_valid():
                return Response(
                    {"errors": input_dto.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            location = self.update_use_case.execute(pk, input_dto.validated_data)

            output_dto = LocationOutputDTO(location)
            return Response(output_dto.to_dict(), status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        """Partial update a location"""
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """Delete a location"""
        try:
            success = self.delete_use_case.execute(pk)

            if success:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND
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
        """Search locations by name"""
        try:
            name = request.query_params.get("name", "")

            if not name:
                return Response(
                    {"error": "Name parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Execute use case
            locations = self.search_use_case.execute(name)

            output_dtos = [LocationOutputDTO(location) for location in locations]
            return Response(
                [dto.to_dict() for dto in output_dtos], status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def rooms(self, request, pk=None):
        """Get a location with its rooms"""
        try:
            # Execute use case
            result = self.get_with_rooms_use_case.execute(pk)

            # Prepare response
            location_dto = LocationOutputDTO(result["location"])
            response_data = location_dto.to_dict()
            response_data["rooms"] = []  # Would need room DTOs here
            response_data["room_count"] = result["room_count"]

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
