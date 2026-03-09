from django.db import models
from clients.utils.id_generator import generate_unique_id


class BaseModel(models.Model):

    unique_id = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if not self.unique_id:
            prefix = self.__class__.__name__.lower()
            self.unique_id = generate_unique_id(prefix)

        super().save(*args, **kwargs)