from rest_framework import serializers
from ...domain.entities.location import Location


class LocationInputDTO(serializers.Serializer):
    """
    DTO for Location input data validation
    """

    name = serializers.CharField(max_length=255)
    address = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_name(self, value):
        """Validate name field"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Name cannot be empty")
        return value.strip()


class LocationOutputDTO:
    """
    DTO for Location output data representation
    """

    def __init__(self, location: Location):
        """Initialize with a Location entity"""
        self.location = location

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON response"""
        return {
            "id": self.location.id,
            "name": self.location.name,
            "address": self.location.address,
            "description": self.location.description,
            "created_at": (
                self.location.created_at.isoformat()
                if self.location.created_at
                else None
            ),
            "updated_at": (
                self.location.updated_at.isoformat()
                if self.location.updated_at
                else None
            ),
        }
