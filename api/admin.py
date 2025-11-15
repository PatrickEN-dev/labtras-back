from django.contrib import admin
from .models import Location, Room, Manager, Booking


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "address")
    readonly_fields = ("id", "created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "capacity", "created_at", "updated_at")
    list_filter = ("location", "capacity", "created_at", "updated_at")
    search_fields = ("name", "description", "location__name")
    readonly_fields = ("id", "created_at", "updated_at")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(deleted_at__isnull=True)
            .select_related("location")
        )


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "email")
    readonly_fields = ("id", "created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "manager",
        "start_date",
        "end_date",
        "coffee_option",
        "created_at",
    )
    list_filter = ("coffee_option", "start_date", "end_date", "created_at")
    search_fields = ("room__name", "manager__name", "manager__email")
    readonly_fields = ("id", "created_at", "updated_at")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(deleted_at__isnull=True)
            .select_related("room", "manager")
        )
