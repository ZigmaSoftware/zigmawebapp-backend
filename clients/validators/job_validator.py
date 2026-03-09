from django.core.exceptions import ValidationError


def validate_title(value):
    if len(value) < 3:
        raise ValidationError("Title must contain at least 3 characters")


def validate_location(value):
    if not isinstance(value, list):
        raise ValidationError("Location must be a list")

    if len(value) == 0:
        raise ValidationError("Location list cannot be empty")


def validate_qualifications(value):
    if not isinstance(value, list):
        raise ValidationError("Qualifications must be a list")

    if len(value) == 0:
        raise ValidationError("Qualifications cannot be empty")


def validate_responsibilities(value):
    if not isinstance(value, list):
        raise ValidationError("Responsibilities must be a list")

    if len(value) == 0:
        raise ValidationError("Responsibilities cannot be empty")