"""
Testes para Use Cases (CQRS).
Testa a orquestração entre services e repositories.
"""

from django.test import TestCase
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from ..use_cases.create_booking import CreateBookingUseCase
from ..use_cases.list_bookings import ListBookingsUseCase
from ..use_cases.update_booking import UpdateBookingUseCase
from ..use_cases.delete_booking import DeleteBookingUseCase
from ..services.booking_service import BookingConflictError


class TestCreateBookingUseCase(TestCase):

    def setUp(self):
        self.use_case = CreateBookingUseCase()
        self.mock_service = Mock()
        self.mock_repository = Mock()
        self.use_case.service = self.mock_service
        self.use_case.repository = self.mock_repository

    def test_execute_successful_creation(self):
        """Testa criação bem-sucedida."""
        # Arrange
        data = {
            "room_id": "room1",
            "manager_id": "manager1",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(hours=2),
            "coffee_option": True,
            "coffee_quantity": 10,
        }

        expected_booking = Mock()
        self.mock_repository.create.return_value = expected_booking

        # Act
        result = self.use_case.execute(data)

        # Assert
        self.mock_service.validate_business_rules.assert_called_once_with(data)
        self.mock_repository.create.assert_called_once()
        self.assertEqual(result, expected_booking)

    def test_execute_with_conflict_error(self):
        """Testa criação com erro de conflito."""
        # Arrange
        data = {"room_id": "room1"}
        self.mock_service.validate_business_rules.side_effect = BookingConflictError(
            "Conflito!"
        )

        # Act & Assert
        with self.assertRaises(BookingConflictError):
            self.use_case.execute(data)

        # Repository não deve ser chamado se houver erro de validação
        self.mock_repository.create.assert_not_called()


class TestListBookingsUseCase(TestCase):

    def setUp(self):
        self.use_case = ListBookingsUseCase()
        self.mock_repository = Mock()
        self.use_case.repository = self.mock_repository

    def test_execute_without_filters(self):
        """Testa listagem sem filtros."""
        # Arrange
        expected_bookings = ["booking1", "booking2"]
        self.mock_repository.list.return_value = expected_bookings

        # Act
        result = self.use_case.execute()

        # Assert
        self.mock_repository.list.assert_called_once_with(None)
        self.assertEqual(result, expected_bookings)

    def test_execute_with_filters(self):
        """Testa listagem com filtros."""
        # Arrange
        filters = {"room_id": "room1"}
        expected_bookings = ["filtered_booking"]
        self.mock_repository.list.return_value = expected_bookings

        # Act
        result = self.use_case.execute(filters)

        # Assert
        self.mock_repository.list.assert_called_once_with(filters)
        self.assertEqual(result, expected_bookings)

    def test_execute_by_room(self):
        """Testa busca por sala específica."""
        # Arrange
        expected_bookings = ["room_booking"]
        self.mock_repository.list.return_value = expected_bookings

        # Act
        result = self.use_case.execute_by_room("room1")

        # Assert
        self.mock_repository.list.assert_called_once_with({"room_id": "room1"})
        self.assertEqual(result, expected_bookings)


class TestUpdateBookingUseCase(TestCase):

    def setUp(self):
        self.use_case = UpdateBookingUseCase()
        self.mock_service = Mock()
        self.mock_repository = Mock()
        self.use_case.service = self.mock_service
        self.use_case.repository = self.mock_repository

    def test_execute_successful_update(self):
        """Testa atualização bem-sucedida."""
        # Arrange
        booking_id = "booking123"
        data = {"start_date": datetime.now()}

        existing_booking = Mock()
        existing_booking.room_id = "room1"
        existing_booking.start_date = datetime.now() - timedelta(hours=1)
        existing_booking.end_date = datetime.now() + timedelta(hours=1)

        updated_booking = Mock()

        self.mock_repository.get.return_value = existing_booking
        self.mock_repository.update.return_value = updated_booking

        # Act
        result = self.use_case.execute(booking_id, data)

        # Assert
        self.mock_service.validate_business_rules.assert_called_once()
        self.mock_repository.update.assert_called_once()
        self.assertEqual(result, updated_booking)

    def test_execute_booking_not_found(self):
        """Testa atualização de reserva inexistente."""
        # Arrange
        self.mock_repository.get.return_value = None

        # Act
        result = self.use_case.execute("nonexistent", {})

        # Assert
        self.assertIsNone(result)
        self.mock_service.validate_business_rules.assert_not_called()
        self.mock_repository.update.assert_not_called()


class TestDeleteBookingUseCase(TestCase):

    def setUp(self):
        self.use_case = DeleteBookingUseCase()
        self.mock_repository = Mock()
        self.use_case.repository = self.mock_repository

    def test_execute_successful_deletion(self):
        """Testa exclusão bem-sucedida."""
        # Arrange
        self.mock_repository.delete.return_value = True

        # Act
        result = self.use_case.execute("booking123")

        # Assert
        self.mock_repository.delete.assert_called_once_with("booking123")
        self.assertTrue(result)

    def test_execute_booking_not_found(self):
        """Testa exclusão de reserva inexistente."""
        # Arrange
        self.mock_repository.delete.return_value = False

        # Act
        result = self.use_case.execute("nonexistent")

        # Assert
        self.assertFalse(result)
