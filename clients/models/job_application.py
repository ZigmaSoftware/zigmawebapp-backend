from django.db import models
from clients.models.base_model import BaseModel
from .job import Job

from clients.validators.job_application_validators import (
    validate_full_name,
    validate_phone,
    validate_resume,
    validate_cover_letter
)

class JobApplication(BaseModel):

    job_id = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
        to_field="unique_id",
        db_column="job_id"
    )

    full_name = models.CharField(
        max_length=255,
        validators=[validate_full_name]
    )

    phone = models.CharField(
        max_length=20,
        validators=[validate_phone]
    )

    email = models.EmailField()

    resume = models.FileField(
        upload_to="resumes/",
        validators=[validate_resume]
    )

    cover_letter = models.TextField(
        blank=True,
        null=True,
        validators=[validate_cover_letter]
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.unique_id} - {self.full_name}"