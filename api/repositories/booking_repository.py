from typing import List, Optional
from django.db.models import Q
from ..models.booking import Booking


class BookingRepository:
    """
    Repository para encapsular operações CRUD de Booking.
    Nunca contém regras de negócio - apenas acesso ao banco.
    """

    @staticmethod
    def list(filters: Optional[dict] = None) -> List[Booking]:
        """Lista todas as reservas com filtros opcionais."""
        queryset = Booking.objects.filter(deleted_at__isnull=True)

        if filters:
            if filters.get("room_id"):
                queryset = queryset.filter(room_id=filters["room_id"])
            if filters.get("manager_id"):
                queryset = queryset.filter(manager_id=filters["manager_id"])
            if filters.get("start_date"):
                queryset = queryset.filter(start_date__gte=filters["start_date"])
            if filters.get("end_date"):
                queryset = queryset.filter(end_date__lte=filters["end_date"])

        return queryset.select_related("room", "manager").order_by("start_date")

    @staticmethod
    def get(booking_id: str) -> Optional[Booking]:
        """Busca uma reserva por ID."""
        try:
            return Booking.objects.select_related("room", "manager").get(
                id=booking_id, deleted_at__isnull=True
            )
        except Booking.DoesNotExist:
            return None

    @staticmethod
    def create(booking_data: dict) -> Booking:
        """Cria uma nova reserva."""
        booking = Booking(**booking_data)
        booking.save()
        return booking

    @staticmethod
    def update(booking_id: str, booking_data: dict) -> Optional[Booking]:
        """Atualiza uma reserva existente."""
        booking = BookingRepository.get(booking_id)
        if not booking:
            return None

        for field, value in booking_data.items():
            setattr(booking, field, value)

        booking.save()
        return booking

    @staticmethod
    def delete(booking_id: str) -> bool:
        """Soft delete de uma reserva."""
        booking = BookingRepository.get(booking_id)
        if not booking:
            return False

        from django.utils import timezone

        booking.deleted_at = timezone.now()
        booking.save()
        return True

    @staticmethod
    def find_conflicts(
        room_id: str, start_date, end_date, exclude_booking_id: str = None
    ) -> List[Booking]:
        """
        Encontra reservas que conflitam com o período especificado.
        Usado pelo service para validação de conflito.
        """
        queryset = Booking.objects.filter(
            room_id=room_id, deleted_at__isnull=True
        ).filter(
            # Conflito: nova reserva começa antes da existente terminar
            # E nova reserva termina depois da existente começar
            Q(start_date__lt=end_date)
            & Q(end_date__gt=start_date)
        )

        # Exclui a própria reserva se estiver atualizando
        if exclude_booking_id:
            queryset = queryset.exclude(id=exclude_booking_id)

        return list(queryset)
