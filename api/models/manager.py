from django.db import models
import uuid


class Manager(models.Model):
    id = models.CharField(
        max_length=25, primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "managers"

    def __str__(self):
        return self.name
