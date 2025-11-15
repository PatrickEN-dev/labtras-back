from datetime import datetime
from typing import Dict, Any
from ..repositories.booking_repository import BookingRepository


class BookingConflictError(Exception):
    """Exceção customizada para conflitos de reserva."""

    pass


class BookingValidationError(Exception):
    """Exceção customizada para erros de validação."""

    pass


class BookingService:
    """
    Service que contém todas as regras de negócio para reservas.
    Não acessa o banco diretamente - usa o repository.
    """

    def __init__(self):
        self.repository = BookingRepository()

    def validate_conflict(self, data: Dict[str, Any]) -> None:
        """
        Valida se existe conflito de horário para a reserva.
        Levanta BookingConflictError se houver conflito.

        Args:
            data: Dados da reserva contendo room_id, start_date, end_date
                 e opcionalmente booking_id (para updates)

        Raises:
            BookingConflictError: Se existir conflito de horário
        """
        room_id = data.get("room_id")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        booking_id = data.get("booking_id")  # Para updates

        # Busca conflitos
        conflicts = self.repository.find_conflicts(
            room_id=room_id,
            start_date=start_date,
            end_date=end_date,
            exclude_booking_id=booking_id,
        )

        if conflicts:
            conflict_details = []
            for conflict in conflicts:
                conflict_details.append(
                    f"Reserva {conflict.id} de {conflict.start_date} até {conflict.end_date}"
                )

            raise BookingConflictError(
                f"Conflito de horário detectado na sala {room_id}. "
                f"Reservas conflitantes: {'; '.join(conflict_details)}"
            )

    def validate_booking_data(self, data: Dict[str, Any]) -> None:
        """
        Valida os dados básicos da reserva.

        Args:
            data: Dados da reserva

        Raises:
            BookingValidationError: Se os dados estiverem inválidos
        """
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Validação de datas
        if not start_date or not end_date:
            raise BookingValidationError("Data de início e fim são obrigatórias")

        if isinstance(start_date, str):
            try:
                start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                data["start_date"] = start_date
            except ValueError:
                raise BookingValidationError("Formato de data de início inválido")

        if isinstance(end_date, str):
            try:
                end_date = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                data["end_date"] = end_date
            except ValueError:
                raise BookingValidationError("Formato de data de fim inválido")

        if start_date >= end_date:
            raise BookingValidationError(
                "Data de início deve ser anterior à data de fim"
            )

        # Validação de café
        if data.get("coffee_option", False):
            coffee_quantity = data.get("coffee_quantity")
            if not coffee_quantity or coffee_quantity <= 0:
                raise BookingValidationError(
                    "Quantidade de café deve ser especificada quando opção café está ativada"
                )

    def validate_business_rules(self, data: Dict[str, Any]) -> None:
        """
        Executa todas as validações de regra de negócio.

        Args:
            data: Dados da reserva

        Raises:
            BookingValidationError: Se alguma regra de negócio for violada
            BookingConflictError: Se houver conflito de horário
        """
        self.validate_booking_data(data)
        self.validate_conflict(data)
