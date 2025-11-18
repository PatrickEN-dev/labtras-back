from rest_framework import serializers
from ...domain.entities.booking import Booking
from ...domain.entities.room import Room
from ...domain.entities.manager import Manager


class BookingInputDTO(serializers.Serializer):
    """
    DTO for Booking input data validation
    """

    room = serializers.CharField()  # Room ID
    manager = serializers.CharField()  # Manager ID
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    coffee_option = serializers.BooleanField(default=False)
    coffee_quantity = serializers.IntegerField(required=False, allow_null=True)
    coffee_description = serializers.CharField(required=False, allow_blank=True)

    def validate_room(self, value):
        """Validate room exists"""
        # Import Django model here to avoid circular imports
        from ...models.room import Room as RoomModel

        if not RoomModel.objects.filter(id=value, deleted_at__isnull=True).exists():
            raise serializers.ValidationError(
                "Selected room does not exist or is deleted"
            )
        return value

    def validate_manager(self, value):
        """Validate manager exists"""
        # Import Django model here to avoid circular imports
        from ...models.manager import Manager as ManagerModel

        if not ManagerModel.objects.filter(id=value, deleted_at__isnull=True).exists():
            raise serializers.ValidationError(
                "Selected manager does not exist or is deleted"
            )
        return value

    def validate(self, data):
        """Cross-field validation"""
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError("Start date must be before end date")

        # Coffee validation
        coffee_option = data.get("coffee_option", False)
        coffee_quantity = data.get("coffee_quantity")

        if coffee_option and not coffee_quantity:
            raise serializers.ValidationError(
                "Coffee quantity is required when coffee option is selected"
            )

        return data


class BookingOutputDTO:
    """
    DTO for Booking output data representation
    """

    def __init__(self, booking: Booking):
        """Initialize with a Booking entity"""
        self.booking = booking

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON response"""
        result = {
            "id": self.booking.id,
            "room_id": self.booking.room_id,
            "manager_id": self.booking.manager_id,
            "name": self.booking.name,
            "description": self.booking.description,
            "start_date": (
                self.booking.start_date.isoformat() if self.booking.start_date else None
            ),
            "end_date": (
                self.booking.end_date.isoformat() if self.booking.end_date else None
            ),
            "coffee_option": self.booking.coffee_option,
            "coffee_quantity": self.booking.coffee_quantity,
            "coffee_description": self.booking.coffee_description,
            "created_at": (
                self.booking.created_at.isoformat() if self.booking.created_at else None
            ),
            "updated_at": (
                self.booking.updated_at.isoformat() if self.booking.updated_at else None
            ),
        }

        # Add room object if available
        if hasattr(self.booking, "room") and self.booking.room:
            result["room"] = {
                "id": self.booking.room.id,
                "name": self.booking.room.name,
                "capacity": self.booking.room.capacity,
                "location_id": self.booking.room.location_id,
            }

        # Add manager object if available
        if hasattr(self.booking, "manager") and self.booking.manager:
            result["manager"] = {
                "id": self.booking.manager.id,
                "name": self.booking.manager.name,
                "email": self.booking.manager.email,
            }

        return result
