from django.db import models
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Location(models.Model):
    id = models.CharField(
        max_length=36, primary_key=True, default=generate_uuid, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "locations"

    def __str__(self):
        return self.name
