"""
Testes para a camada de serviços.
Foca nas regras de negócio, especialmente validação de conflitos.
"""

import pytest
from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from unittest.mock import Mock, patch
from ..services.booking_service import (
    BookingService,
    BookingConflictError,
    BookingValidationError,
)


class TestBookingService(TestCase):

    def setUp(self):
        self.service = BookingService()
        self.mock_repository = Mock()
        self.service.repository = self.mock_repository

    def test_validate_conflict_no_conflicts(self):
        """Testa validação quando não há conflitos."""
        # Arrange
        self.mock_repository.find_conflicts.return_value = []
        data = {
            "room_id": "room1",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(hours=2),
        }

        # Act & Assert - não deve levantar exceção
        try:
            self.service.validate_conflict(data)
        except BookingConflictError:
            self.fail("validate_conflict raised BookingConflictError unexpectedly")

    def test_validate_conflict_with_conflicts(self):
        """Testa validação quando há conflitos."""
        # Arrange
        conflict_booking = Mock()
        conflict_booking.id = "booking123"
        conflict_booking.start_date = datetime.now()
        conflict_booking.end_date = datetime.now() + timedelta(hours=2)

        self.mock_repository.find_conflicts.return_value = [conflict_booking]

        data = {
            "room_id": "room1",
            "start_date": datetime.now() + timedelta(hours=1),
            "end_date": datetime.now() + timedelta(hours=3),
        }

        # Act & Assert
        with pytest.raises(BookingConflictError) as exc_info:
            self.service.validate_conflict(data)

        self.assertIn("Conflito de horário detectado", str(exc_info.value))
        self.assertIn("booking123", str(exc_info.value))

    def test_validate_booking_data_missing_dates(self):
        """Testa validação com datas faltando."""
        data = {"room_id": "room1"}

        with pytest.raises(BookingValidationError) as exc_info:
            self.service.validate_booking_data(data)

        self.assertIn("obrigatórias", str(exc_info.value))

    def test_validate_booking_data_invalid_date_order(self):
        """Testa validação com data de início após data de fim."""
        data = {
            "start_date": datetime.now() + timedelta(hours=2),
            "end_date": datetime.now(),
        }

        with pytest.raises(BookingValidationError) as exc_info:
            self.service.validate_booking_data(data)

        self.assertIn("anterior", str(exc_info.value))

    def test_validate_booking_data_coffee_without_quantity(self):
        """Testa validação de café sem quantidade."""
        data = {
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(hours=2),
            "coffee_option": True,
            "coffee_quantity": None,
        }

        with pytest.raises(BookingValidationError) as exc_info:
            self.service.validate_booking_data(data)

        self.assertIn("café deve ser especificada", str(exc_info.value))

    def test_validate_business_rules_calls_all_validations(self):
        """Testa que validate_business_rules chama todas as validações."""
        with patch.object(self.service, "validate_booking_data") as mock_validate_data:
            with patch.object(
                self.service, "validate_conflict"
            ) as mock_validate_conflict:
                data = {"test": "data"}

                self.service.validate_business_rules(data)

                mock_validate_data.assert_called_once_with(data)
                mock_validate_conflict.assert_called_once_with(data)
