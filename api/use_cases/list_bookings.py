from typing import List, Dict, Any, Optional
from ..repositories.booking_repository import BookingRepository
from ..models.booking import Booking


class ListBookingsUseCase:
    """
    Use Case para listagem de reservas.
    Implementa o padrão Query do CQRS.
    """

    def __init__(self):
        self.repository = BookingRepository()

    def execute(self, filters: Optional[Dict[str, Any]] = None) -> List[Booking]:
        """
        Executa a listagem de reservas com filtros opcionais.

        Args:
            filters: Filtros para aplicar na busca
                    - room_id: ID da sala
                    - manager_id: ID do responsável
                    - start_date: Data inicial mínima
                    - end_date: Data final máxima

        Returns:
            List[Booking]: Lista de reservas encontradas
        """
        # Para queries, não há validação complexa de negócio
        # Apenas aplicamos os filtros e retornamos
        return self.repository.list(filters)

    def execute_by_room(self, room_id: str) -> List[Booking]:
        """
        Busca reservas específicas de uma sala.
        """
        filters = {"room_id": room_id}
        return self.execute(filters)

    def execute_by_manager(self, manager_id: str) -> List[Booking]:
        """
        Busca reservas específicas de um responsável.
        """
        filters = {"manager_id": manager_id}
        return self.execute(filters)

    def execute_by_period(self, start_date, end_date) -> List[Booking]:
        """
        Busca reservas em um período específico.
        """
        filters = {"start_date": start_date, "end_date": end_date}
        return self.execute(filters)
