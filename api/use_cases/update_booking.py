from typing import Dict, Any, Optional
from ..repositories.booking_repository import BookingRepository
from ..services.booking_service import BookingService
from ..models.booking import Booking


class UpdateBookingUseCase:
    """
    Use Case para atualização de reservas.
    Implementa o padrão Command do CQRS.
    """

    def __init__(self):
        self.repository = BookingRepository()
        self.service = BookingService()

    def execute(self, booking_id: str, data: Dict[str, Any]) -> Optional[Booking]:
        """
        Executa a atualização de uma reserva existente.

        Args:
            booking_id: ID da reserva a ser atualizada
            data: Novos dados da reserva

        Returns:
            Booking: Instância da reserva atualizada ou None se não encontrada

        Raises:
            BookingValidationError: Se os dados forem inválidos
            BookingConflictError: Se houver conflito de horário
        """
        # 1. Verificar se a reserva existe
        existing_booking = self.repository.get(booking_id)
        if not existing_booking:
            return None

        # 2. Preparar dados com o ID da reserva para validação de conflito
        validation_data = data.copy()
        validation_data["booking_id"] = booking_id

        # Usar dados existentes se não fornecidos
        validation_data.setdefault("room_id", existing_booking.room_id)
        validation_data.setdefault("start_date", existing_booking.start_date)
        validation_data.setdefault("end_date", existing_booking.end_date)

        # 3. Validar regras de negócio
        self.service.validate_business_rules(validation_data)

        # 4. Preparar dados para persistência
        update_data = self._prepare_update_data(data)

        # 5. Atualizar no banco
        updated_booking = self.repository.update(booking_id, update_data)

        return updated_booking

    def _prepare_update_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara os dados para atualização, removendo campos não permitidos.
        """
        allowed_fields = {
            "room_id",
            "manager_id",
            "start_date",
            "end_date",
            "coffee_option",
            "coffee_quantity",
            "coffee_description",
        }

        return {
            field: value for field, value in data.items() if field in allowed_fields
        }
