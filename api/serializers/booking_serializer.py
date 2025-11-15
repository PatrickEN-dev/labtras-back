from rest_framework import serializers
from ..models.booking import Booking
from ..models.room import Room
from ..models.manager import Manager


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Booking.
    Usa ModelSerializer conforme especificado.
    """

    # Campos read-only para exibir informações relacionadas
    room_name = serializers.CharField(source="room.name", read_only=True)
    room_location = serializers.CharField(source="room.location.name", read_only=True)
    manager_name = serializers.CharField(source="manager.name", read_only=True)
    manager_email = serializers.CharField(source="manager.email", read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at")

    def validate(self, data):
        """
        Validação customizada dos dados do serializer.
        """
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Validação básica de datas
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("Start date must be before end date")

        # Validação de café
        if data.get("coffee_option", False):
            coffee_quantity = data.get("coffee_quantity")
            if not coffee_quantity or coffee_quantity <= 0:
                raise serializers.ValidationError(
                    "Coffee quantity must be specified when coffee option is enabled"
                )

        return data

    def validate_room(self, value):
        """
        Validação do campo room.
        """
        if not Room.objects.filter(id=value.id, deleted_at__isnull=True).exists():
            raise serializers.ValidationError(
                "Selected room does not exist or is deleted"
            )
        return value

    def validate_manager(self, value):
        """
        Validação do campo manager.
        """
        if not Manager.objects.filter(id=value.id, deleted_at__isnull=True).exists():
            raise serializers.ValidationError(
                "Selected manager does not exist or is deleted"
            )
        return value

    def to_representation(self, instance):
        """
        Customiza a representação da saída para incluir dados relacionados.
        """
        representation = super().to_representation(instance)

        # Remover campos de soft delete da resposta
        representation.pop("deleted_at", None)

        return representation
