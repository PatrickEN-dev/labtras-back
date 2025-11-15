from ..repositories.booking_repository import BookingRepository


class DeleteBookingUseCase:
    """
    Use Case para exclusão de reservas.
    Implementa o padrão Command do CQRS.
    """

    def __init__(self):
        self.repository = BookingRepository()

    def execute(self, booking_id: str) -> bool:
        """
        Executa a exclusão (soft delete) de uma reserva.

        Args:
            booking_id: ID da reserva a ser excluída

        Returns:
            bool: True se a reserva foi excluída, False se não encontrada
        """
        # Para exclusão, não há regras complexas de negócio
        # Apenas verificamos se existe e fazemos soft delete
        return self.repository.delete(booking_id)
