from django.db.models import Q
from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import FootballField, FieldImage, Reservation
from rest_framework.serializers import ModelSerializer


class FieldImageSerializers(ModelSerializer):
    class Meta:
        model = FieldImage
        fields = ['image']


class FootballFieldSerializers(ModelSerializer):
    images = FieldImageSerializers(many=True, read_only=True)
    distance = serializers.FloatField(default=0)

    class Meta:
        model = FootballField
        fields = ['id', 'name', 'address', 'contact', 'price_per_hour', 'images', 'owner', 'latitude', 'longitude',
                  'distance']
        extra_kwargs = {
            'owner': {'required': False},
        }


class FootballFieldSerializersUpdate(ModelSerializer):
    images = FieldImageSerializers(many=True, read_only=True)

    class Meta:
        model = FootballField
        fields = ['id', 'name', 'address', 'contact', 'price_per_hour', 'images', 'owner', 'latitude', 'longitude']
        extra_kwargs = {
            'owner': {'required': False},
            'name': {'required': False},
            'address': {'required': False},
            'contact': {'required': False},
            'price_per_hour': {'required': False},
            'images': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
        }


class ReservationSerializers(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['field', 'date', 'start_time', 'end_time']
        extra_kwargs = {
            'field': {'required': True},
            'date': {'required': True},
            'start_time': {'required': True},
            'end_time': {'required': True},
        }

    def save(self, **kwargs):
        start_time = self.validated_data['start_time']
        end_time = self.validated_data['end_time']
        date = self.validated_data['date']
        field = self.validated_data['field']

        # check if the start time is less than the end time
        if start_time > end_time:
            raise serializers.ValidationError('End time must be less than start time')
        # check if the reservation already exists
        if Reservation.objects.filter(
                Q(start_time__gte=start_time, end_time__lte=end_time) |
                Q(start_time__gt=start_time, start_time__lt=end_time) |
                Q(end_time__gt=start_time, end_time__lt=end_time)):
            raise serializers.ValidationError('Reservation already exists')
        """
        Checks if there is a reservation for the given date and time. If there is, it adds the given field.
         Otherwise, it creates a new reservation.
        """
        if Reservation.objects.filter(start_time=start_time, end_time=end_time, date=date).exists():
            reservations = Reservation.objects.filter(start_time=start_time, end_time=end_time, date=date).last()
            reservations.field.add(field[0])
            return reservations
        return super().save(**kwargs)


class FootballReservation(ModelSerializer):
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = FootballField
        fields = ['name', 'address', 'owner']


class ReservationSerializersResponse(ModelSerializer):
    # field = FootballReservation(many=True)

    class Meta:
        model = Reservation
        fields = ['id', 'field', 'date', 'start_time', 'end_time']
