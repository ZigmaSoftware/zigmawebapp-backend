from django.db import models
from clients.models.base_model import BaseModel
from clients.validators.job_validator import (
    validate_title,
    validate_location,
    validate_qualifications,
    validate_responsibilities
)


class Job(BaseModel):

    title = models.CharField(
        max_length=255,
        validators=[validate_title]
    )

    department = models.CharField(max_length=100)

    location = models.JSONField(
        validators=[validate_location]
    )

    job_type = models.CharField(max_length=50)

    experience_required = models.CharField(max_length=100)

    qualifications = models.JSONField(
        validators=[validate_qualifications]
    )

    responsibilities = models.JSONField(
        validators=[validate_responsibilities]
    )

    def __str__(self):
        return f"{self.unique_id} - {self.title}"