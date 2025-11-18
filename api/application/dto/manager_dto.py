from rest_framework import serializers
from ...domain.entities.manager import Manager


class ManagerInputDTO(serializers.Serializer):
    """
    DTO for Manager input data validation
    """

    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_name(self, value):
        """Validate name field"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Name cannot be empty")
        return value.strip()

    def validate_email(self, value):
        """Validate email field"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Email cannot be empty")
        return value.strip().lower()


class ManagerOutputDTO:
    """
    DTO for Manager output data representation
    """

    def __init__(self, manager: Manager):
        """Initialize with a Manager entity"""
        self.manager = manager

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON response"""
        return {
            "id": self.manager.id,
            "name": self.manager.name,
            "email": self.manager.email,
            "phone": self.manager.phone,
            "created_at": (
                self.manager.created_at.isoformat() if self.manager.created_at else None
            ),
            "updated_at": (
                self.manager.updated_at.isoformat() if self.manager.updated_at else None
            ),
        }

    def to_representation(self, instance):
        """Customize output representation"""
        representation = super().to_representation(instance)
        representation.pop("deleted_at", None)
        return representation
