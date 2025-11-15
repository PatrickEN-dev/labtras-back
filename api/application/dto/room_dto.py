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
        if not Location.objects.filter(id=value, deleted_at__isnull=True).exists():
            raise serializers.ValidationError(
                "Selected location does not exist or is deleted"
            )
        return value


class RoomOutputDTO(serializers.ModelSerializer):
    """
    DTO for Room output data representation
    """

    location_name = serializers.CharField(source="location.name", read_only=True)
    location_address = serializers.CharField(source="location.address", read_only=True)
    active_bookings_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "capacity",
            "description",
            "location",
            "location_name",
            "location_address",
            "active_bookings_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "location_name",
            "location_address",
        ]

    def get_active_bookings_count(self, obj):
        """Get count of active bookings"""
        return obj.get_active_bookings_count()

    def to_representation(self, instance):
        """Customize output representation"""
        representation = super().to_representation(instance)
        representation.pop("deleted_at", None)
        return representation
