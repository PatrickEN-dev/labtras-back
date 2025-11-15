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


class LocationOutputDTO(serializers.ModelSerializer):
    """
    DTO for Location output data representation
    """

    active_rooms_count = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "address",
            "description",
            "active_rooms_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_active_rooms_count(self, obj):
        """Get count of active rooms"""
        return obj.get_active_rooms_count()

    def to_representation(self, instance):
        """Customize output representation"""
        representation = super().to_representation(instance)
        # Remove soft delete fields from response
        representation.pop("deleted_at", None)
        return representation
