from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .infrastructure.viewsets.booking_viewset import BookingViewSet
from .infrastructure.viewsets.location_viewset import LocationViewSet
from .infrastructure.viewsets.room_viewset import RoomViewSet
from .infrastructure.viewsets.manager_viewset import ManagerViewSet

# Configurar router do DRF
router = DefaultRouter()
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"managers", ManagerViewSet, basename="manager")
router.register(r"bookings", BookingViewSet, basename="booking")

# URLs da API
urlpatterns = [
    # Router padrão que cria automaticamente:
    # /locations/ - GET (list), POST (create)
    # /locations/{id}/ - GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
    # /rooms/ - GET (list), POST (create)
    # /rooms/{id}/ - GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
    # /rooms/by_location/ - GET (custom action)
    # /managers/ - GET (list), POST (create)
    # /managers/{id}/ - GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
    # /managers/by_email/ - GET (custom action)
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
                path(
                    "",
                    include(
                        [
                            path(
                                "",
                                BookingViewSet.as_view(
                                    {"get": "list", "post": "create"}
                                ),
                            ),
                            path(
                                "<str:pk>/",
                                BookingViewSet.as_view(
                                    {
                                        "get": "retrieve",
                                        "put": "update",
                                        "patch": "partial_update",
                                        "delete": "destroy",
                                    }
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
