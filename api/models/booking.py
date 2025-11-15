from django.db import models
import uuid
from .room import Room
from .manager import Manager


class Booking(models.Model):
    id = models.CharField(
        max_length=25, primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="bookings", db_column="room_id"
    )
    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        related_name="bookings",
        db_column="manager_id",
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    coffee_option = models.BooleanField(default=False)
    coffee_quantity = models.IntegerField(null=True, blank=True)
    coffee_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "bookings"

    def __str__(self):
        return f"{self.room.name} - {self.start_date} to {self.end_date}"

    def save(self, *args, **kwargs):
        # Validação básica de data
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        super().save(*args, **kwargs)
