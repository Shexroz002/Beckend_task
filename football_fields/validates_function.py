import math

from django.core.exceptions import ValidationError
from users.models import CustomUser


def price_per_hour_validator(value):
    if value < 0:
        raise ValidationError("Title length should be below 100 characters.")


def validate_owner(value):
    if value is None:
        raise ValidationError("Owner must be identified.")
    if isinstance(value, CustomUser):

        if CustomUser.objects.filter(id=value.id).last().role not in ['field_owner', 'admin']:
            raise ValidationError("Owner must be a field owner.")
    elif isinstance(value, int):
        if CustomUser.objects.filter(id=value).last().role not in ['field_owner', 'admin']:
            raise ValidationError("Owner must be a field owner.")


def validate_image_size(value):
    max_size = 50 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("Image size should be below 50 MB.")
