from rest_framework import serializers
from ...domain.entities.room import Room
from ...domain.entities.location import Location


class RoomInputDTO(serializers.Serializer):
    """
    DTO for Room input data validation
    """

    name = serializers.CharField(max_length=255)
    capacity = serializers.IntegerField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField()  # Location ID

    def validate_name(self, value):
        """Validate name field"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Name cannot be empty")
        return value.strip()

    def validate_capacity(self, value):
        """Validate capacity field"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0")
        return value

    def validate_location(self, value):
        """Validate location exists"""

        from ...models.location import Location as LocationModel

        if not LocationModel.objects.filter(id=value, deleted_at__isnull=True).exists():
            raise serializers.ValidationError(
                "Selected location does not exist or is deleted"
            )
        return value


class RoomOutputDTO:
    """
    DTO for Room output data representation
    """

    def __init__(self, room: Room):
        """Initialize with a Room entity"""
        self.room = room

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON response"""
        return {
            "id": self.room.id,
            "name": self.room.name,
            "capacity": self.room.capacity,
            "description": self.room.description,
            "location_id": self.room.location_id,
            "created_at": (
                self.room.created_at.isoformat() if self.room.created_at else None
            ),
            "updated_at": (
                self.room.updated_at.isoformat() if self.room.updated_at else None
            ),
        }
