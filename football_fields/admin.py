from django.contrib import admin
from .models import FootballField, FieldImage, Reservation
# Register your models here.

admin.site.register(FootballField)
admin.site.register(FieldImage)
admin.site.register(Reservation)