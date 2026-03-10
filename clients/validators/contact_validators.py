import re
from django.core.exceptions import ValidationError


def validate_name(value):
    if len(value.strip()) < 3:
        raise ValidationError("Name must contain atleast 3 characters")


def validate_phone(value):
    pattern = r'^[6-9]\d{9}$'

    if not re.match(pattern, value):
        raise ValidationError("Enter a valid 10 digit phone number")


def validate_message(value):
    if len(value.strip()) < 10:
        raise ValidationError("Message must contain atleast 10 characters")