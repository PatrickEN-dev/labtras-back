from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404
from ..serializers.booking_serializer import BookingSerializer
from ..use_cases.create_booking import CreateBookingUseCase
from ..use_cases.list_bookings import ListBookingsUseCase
from ..use_cases.update_booking import UpdateBookingUseCase
from ..use_cases.delete_booking import DeleteBookingUseCase
from ..services.booking_service import BookingConflictError, BookingValidationError


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet para reservas seguindo padrão DRF.
    Usa os use cases para processar cada ação - nunca contém lógica de negócio.
    """

    serializer_class = BookingSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_use_case = CreateBookingUseCase()
        self.list_use_case = ListBookingsUseCase()
        self.update_use_case = UpdateBookingUseCase()
        self.delete_use_case = DeleteBookingUseCase()

    def get_queryset(self):
        """
        Retorna queryset vazio - usamos use cases para buscar dados.
        """
        # Necessário para o DRF, mas não usado diretamente
        from ..models.booking import Booking

        return Booking.objects.none()

    def list(self, request):
        """
        Lista todas as reservas com filtros opcionais.
        Implementa o padrão Query do CQRS.
        """
        try:
            # Extrair filtros dos query parameters
            filters = self._extract_filters(request.query_params)

            # Usar o use case para buscar dados
            bookings = self.list_use_case.execute(filters)

            # Serializar e retornar
            serializer = self.serializer_class(bookings, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        Cria uma nova reserva.
        Implementa o padrão Command do CQRS.
        """
        try:
            # Validar dados de entrada
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Usar o use case para criar
            booking = self.create_use_case.execute(serializer.validated_data)

            # Retornar dados criados
            response_serializer = self.serializer_class(booking)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except BookingConflictError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except BookingValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """
        Busca uma reserva específica por ID.
        """
        try:
            # Usar repository diretamente para busca simples
            from ..repositories.booking_repository import BookingRepository

            booking = BookingRepository.get(pk)

            if not booking:
                raise Http404("Booking not found")

            serializer = self.serializer_class(booking)
            return Response(serializer.data)

        except Http404:
            return Response(
                {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        """
        Atualiza uma reserva existente.
        Implementa o padrão Command do CQRS.
        """
        try:
            # Validar dados de entrada
            serializer = self.serializer_class(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Usar o use case para atualizar
            booking = self.update_use_case.execute(pk, serializer.validated_data)

            if not booking:
                return Response(
                    {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Retornar dados atualizados
            response_serializer = self.serializer_class(booking)
            return Response(response_serializer.data)

        except BookingConflictError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except BookingValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        """
        Exclui (soft delete) uma reserva.
        Implementa o padrão Command do CQRS.
        """
        try:
            # Usar o use case para excluir
            success = self.delete_use_case.execute(pk)

            if not success:
                return Response(
                    {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def by_room(self, request):
        """
        Endpoint customizado para buscar reservas por sala.
        """
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response(
                {"error": "room_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bookings = self.list_use_case.execute_by_room(room_id)
            serializer = self.serializer_class(bookings, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def by_manager(self, request):
        """
        Endpoint customizado para buscar reservas por responsável.
        """
        manager_id = request.query_params.get("manager_id")
        if not manager_id:
            return Response(
                {"error": "manager_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bookings = self.list_use_case.execute_by_manager(manager_id)
            serializer = self.serializer_class(bookings, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def _extract_filters(self, query_params):
        """
        Extrai filtros dos parâmetros de query.
        """
        filters = {}

        if query_params.get("room_id"):
            filters["room_id"] = query_params["room_id"]

        if query_params.get("manager_id"):
            filters["manager_id"] = query_params["manager_id"]

        if query_params.get("start_date"):
            filters["start_date"] = query_params["start_date"]

        if query_params.get("end_date"):
            filters["end_date"] = query_params["end_date"]

        return filters
