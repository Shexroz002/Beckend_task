import math

from django.db import models
from users.models import CustomUser
from .query_set import FootballFieldQuerySet
from .validates_function import price_per_hour_validator, validate_owner, validate_image_size


class FootballFieldManager(models.Manager):
    def get_queryset(self):
        return FootballFieldQuerySet(self.model, using=self._db)

    def annotate_distance(self, target_latitude, target_longitude):
        return self.get_queryset().annotate_distance(target_latitude, target_longitude)


class FootballField(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, default='Name not identified')
    address = models.CharField(max_length=100, null=False, blank=False)
    contact = models.CharField(max_length=13, null=False, blank=False)
    price_per_hour = models.FloatField(null=False, blank=False, validators=[price_per_hour_validator])
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fields', null=False, blank=False,
                              validators=[validate_owner])
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    objects = FootballFieldManager()

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

    def calculate_distance(self, a_latitude, b_longitude):
        if a_latitude is None or b_longitude is None:
            return 0
        return math.sqrt((a_latitude - self.latitude) ** 2 + (b_longitude - self.longitude) ** 2)


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
