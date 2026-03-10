import os
import re
from django.core.exceptions import ValidationError


def validate_full_name(value):
    if len(value.strip()) < 3:
        raise ValidationError("Full name must contain atleast 3 characters")


def validate_phone(value):
    pattern = r'^[6-9]\d{9}$'

    if not re.match(pattern, value):
        raise ValidationError("Enter a valid 10 digit phone number")


def validate_resume(value):
    allowed_extensions = ['.pdf', '.doc', '.docx']
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError("Resume must be a PDF, DOC, or DOCX file")

    max_size = 5 * 1024 * 1024  # 5MB

    if value.size > max_size:
        raise ValidationError("Resume file size must be under 5MB")


def validate_cover_letter(value):
    if value and len(value.strip()) < 10:
        raise ValidationError("Cover letter must contain atleast 10 characters")