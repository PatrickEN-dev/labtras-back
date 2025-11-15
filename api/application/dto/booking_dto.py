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
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    coffee_option = serializers.BooleanField(default=False)
    coffee_quantity = serializers.IntegerField(required=False, allow_null=True)
    coffee_description = serializers.CharField(required=False, allow_blank=True)

    def validate_room(self, value):
        """Validate room exists"""
        if not Room.objects.filter(id=value, deleted_at__isnull=True).exists():
            raise serializers.ValidationError(
                "Selected room does not exist or is deleted"
            )
        return value

    def validate_manager(self, value):
        """Validate manager exists"""
        if not Manager.objects.filter(id=value, deleted_at__isnull=True).exists():
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


class BookingOutputDTO(serializers.ModelSerializer):
    """
    DTO for Booking output data representation
    """

    room_name = serializers.CharField(source="room.name", read_only=True)
    room_location = serializers.CharField(source="room.location.name", read_only=True)
    manager_name = serializers.CharField(source="manager.name", read_only=True)
    manager_email = serializers.CharField(source="manager.email", read_only=True)
    duration_hours = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "room",
            "room_name",
            "room_location",
            "manager",
            "manager_name",
            "manager_email",
            "start_date",
            "end_date",
            "duration_hours",
            "coffee_option",
            "coffee_quantity",
            "coffee_description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "room_name",
            "room_location",
            "manager_name",
            "manager_email",
        ]

    def get_duration_hours(self, obj):
        """Get booking duration in hours"""
        return obj.duration_hours

    def get_status(self, obj):
        """Get booking status"""
        if obj.is_current:
            return "current"
        elif obj.is_future:
            return "scheduled"
        else:
            return "completed"

    def to_representation(self, instance):
        """Customize output representation"""
        representation = super().to_representation(instance)
        representation.pop("deleted_at", None)
        return representation
