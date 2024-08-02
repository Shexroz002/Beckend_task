from django.db import models
from users.models import CustomUser
from .validates_function import price_per_hour_validator, validate_owner, validate_image_size


class FootballField(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, default='Name not identified')
    address = models.CharField(max_length=100, null=False, blank=False)
    contact = models.CharField(max_length=13, null=False, blank=False)
    price_per_hour = models.FloatField(null=False, blank=False, validators=[price_per_hour_validator])
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fields', null=False, blank=False,
                              validators=[validate_owner])
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Football Field'
        verbose_name_plural = 'Football Fields'
        db_table = 'football_fields'
        # Since there is a lot of search and filter with name and address, it is necessary to index
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['address']),
        ]


class FieldImage(models.Model):
    field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='images', null=False, blank=False)
    image = models.ImageField(upload_to='field_images/', null=False, blank=False, validators=[validate_image_size])

    def __str__(self):
        return self.field.name

    class Meta:
        verbose_name = 'Field Image'
        verbose_name_plural = 'Field Images'
        db_table = 'field_images'


class Reservation(models.Model):
    field = models.ManyToManyField(FootballField, related_name='reservations')
    date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date} - {self.start_time} - {self.end_time}'

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        db_table = 'reservations'
        # Since there is a lot of search and filter with start_time and end_time, it is necessary to index
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
        ]

