from django.db import models
from clients.models.base_model import BaseModel
from clients.validators.contact_validators import (
    validate_name,
    validate_phone,
    validate_message
)


class InquiryCategory(models.TextChoices):

    SALES_PARTNERSHIPS = "sales_partnerships", "Sales & Partnerships Alliances"
    GENERAL_INQUIRY = "general_inquiry", "General Inquiry"
    INVESTOR_RELATIONS = "investor_relations", "Investor Relations"


class ContactUs(BaseModel):

    name = models.CharField(
        max_length=255,
        validators=[validate_name]
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        validators=[validate_phone]
    )

    category = models.CharField(
        max_length=50,
        choices=InquiryCategory.choices
    )

    message = models.TextField(
        validators=[validate_message]
    )

    def __str__(self):
        return f"{self.unique_id} - {self.name}"