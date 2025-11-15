from typing import Dict, Any
from ..repositories.booking_repository import BookingRepository
from ..services.booking_service import BookingService
from ..models.booking import Booking


class CreateBookingUseCase:
    """
    Use Case para criação de reservas.
    Implementa o padrão Command do CQRS.
    """

    def __init__(self):
        self.repository = BookingRepository()
        self.service = BookingService()

    def execute(self, data: Dict[str, Any]) -> Booking:
        """
        Executa a criação de uma nova reserva.

        Args:
            data: Dados da reserva vindos da API

        Returns:
            Booking: Instância da reserva criada

        Raises:
            BookingValidationError: Se os dados forem inválidos
            BookingConflictError: Se houver conflito de horário
        """
        # 1. Validar regras de negócio
        self.service.validate_business_rules(data)

        # 2. Preparar dados para persistência
        booking_data = self._prepare_booking_data(data)

        # 3. Persistir no banco
        booking = self.repository.create(booking_data)

        return booking

    def _prepare_booking_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara os dados para criação no formato esperado pelo model.
        """
        return {
            "room_id": data["room_id"],
            "manager_id": data["manager_id"],
            "start_date": data["start_date"],
            "end_date": data["end_date"],
            "coffee_option": data.get("coffee_option", False),
            "coffee_quantity": data.get("coffee_quantity"),
            "coffee_description": data.get("coffee_description"),
        }
