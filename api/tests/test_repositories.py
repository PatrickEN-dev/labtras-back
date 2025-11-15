"""
Testes para a camada de repositórios.
Testa operações CRUD básicas.
"""

from django.test import TestCase
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from ..repositories.booking_repository import BookingRepository
from ..models.booking import Booking


class TestBookingRepository(TestCase):

    def setUp(self):
        self.repository = BookingRepository()

    @patch("api.repositories.booking_repository.Booking.objects")
    def test_list_with_no_filters(self, mock_objects):
        """Testa listagem sem filtros."""
        # Arrange
        mock_queryset = Mock()
        mock_objects.filter.return_value = mock_queryset
        mock_queryset.select_related.return_value = mock_queryset
        mock_queryset.order_by.return_value = ["booking1", "booking2"]

        # Act
        result = self.repository.list()

        # Assert
        mock_objects.filter.assert_called_with(deleted_at__isnull=True)
        self.assertEqual(result, ["booking1", "booking2"])

    @patch("api.repositories.booking_repository.Booking.objects")
    def test_list_with_filters(self, mock_objects):
        """Testa listagem com filtros."""
        # Arrange
        mock_queryset = Mock()
        mock_objects.filter.return_value = mock_queryset
        mock_queryset.filter.return_value = mock_queryset
        mock_queryset.select_related.return_value = mock_queryset
        mock_queryset.order_by.return_value = ["filtered_booking"]

        filters = {"room_id": "room1", "manager_id": "manager1"}

        # Act
        result = self.repository.list(filters)

        # Assert
        self.assertEqual(result, ["filtered_booking"])

    @patch("api.repositories.booking_repository.Booking.objects")
    def test_get_existing_booking(self, mock_objects):
        """Testa busca de reserva existente."""
        # Arrange
        expected_booking = Mock()
        mock_objects.select_related.return_value.get.return_value = expected_booking

        # Act
        result = self.repository.get("booking123")

        # Assert
        mock_objects.select_related.assert_called_with("room", "manager")
        self.assertEqual(result, expected_booking)

    @patch("api.repositories.booking_repository.Booking.objects")
    def test_get_non_existing_booking(self, mock_objects):
        """Testa busca de reserva inexistente."""
        # Arrange
        from ..models.booking import Booking

        mock_objects.select_related.return_value.get.side_effect = (
            Booking.DoesNotExist()
        )

        # Act
        result = self.repository.get("nonexistent")

        # Assert
        self.assertIsNone(result)

    @patch("api.repositories.booking_repository.Booking")
    def test_create_booking(self, mock_booking_class):
        """Testa criação de reserva."""
        # Arrange
        mock_booking = Mock()
        mock_booking_class.return_value = mock_booking

        booking_data = {
            "room_id": "room1",
            "manager_id": "manager1",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(hours=2),
        }

        # Act
        result = self.repository.create(booking_data)

        # Assert
        mock_booking_class.assert_called_once_with(**booking_data)
        mock_booking.save.assert_called_once()
        self.assertEqual(result, mock_booking)

    def test_find_conflicts_logic(self):
        """Testa a lógica de detecção de conflitos."""
        # Este teste verifica se a query de conflitos está sendo construída corretamente
        with patch(
            "api.repositories.booking_repository.Booking.objects"
        ) as mock_objects:
            mock_queryset = Mock()
            mock_objects.filter.return_value = mock_queryset
            mock_queryset.filter.return_value = mock_queryset
            mock_queryset.exclude.return_value = ["conflict1"]

            start_date = datetime.now()
            end_date = start_date + timedelta(hours=2)

            # Act
            result = self.repository.find_conflicts(
                room_id="room1",
                start_date=start_date,
                end_date=end_date,
                exclude_booking_id="booking123",
            )

            # Assert
            self.assertEqual(result, ["conflict1"])
            mock_queryset.exclude.assert_called_with(id="booking123")
