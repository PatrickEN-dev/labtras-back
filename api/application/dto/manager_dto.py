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


class ManagerOutputDTO(serializers.ModelSerializer):
    """
    DTO for Manager output data representation
    """

    active_bookings_count = serializers.SerializerMethodField()

    class Meta:
        model = Manager
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "active_bookings_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_active_bookings_count(self, obj):
        """Get count of active bookings"""
        return obj.get_active_bookings_count()

    def to_representation(self, instance):
        """Customize output representation"""
        representation = super().to_representation(instance)
        representation.pop("deleted_at", None)
        return representation
