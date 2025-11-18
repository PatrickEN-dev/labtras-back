from django.db import models
import uuid
from .location import Location


def generate_uuid():
    return str(uuid.uuid4())


class Room(models.Model):
    id = models.CharField(
        max_length=36, primary_key=True, default=generate_uuid, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=255)
    capacity = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="rooms",
        db_column="location_id",
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "rooms"

    def __str__(self):
        return f"{self.name} - {self.location.name}"
