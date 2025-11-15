from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.booking_view import BookingViewSet

# Configurar router do DRF
router = DefaultRouter()
router.register(r"bookings", BookingViewSet, basename="booking")

# URLs da API
urlpatterns = [
    # Router padrão que cria automaticamente:
    # /bookings/ - GET (list), POST (create)
    # /bookings/{id}/ - GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
    # /bookings/by_room/ - GET (custom action)
    # /bookings/by_manager/ - GET (custom action)
    path("", include(router.urls)),
]

# Também podemos criar aliases para usar "reservations" se preferir
urlpatterns += [
    path(
        "reservations/",
        include(
            [
                path("", include(router.urls)),
            ]
        ),
    ),
]
