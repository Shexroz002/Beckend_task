import math
from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, views, response
from .models import FootballField, Reservation
from .serializers import FootballFieldSerializers, ReservationSerializers, \
    FootballFieldSerializersUpdate, ReservationSerializersResponse
from users.permission import IsAdminAndUser, IsUser, IsAdminAndFieldOwner, get_authentication_user
from .pagination import CustomPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .schame import football_fields_schema_create, football_fields_schema_response, reservation_create_schema, \
    reservation_list_schema


class FootballCreateView(views.APIView):
    permission_classes = [IsAdminAndFieldOwner]

    @swagger_auto_schema(
        operation_description="Create a new football field",
        request_body=football_fields_schema_create,
        responses={
            200: football_fields_schema_response,
            400: 'Bad request',
            403: 'Forbidden',
            201: 'Created'
        }
    )
    def post(self, request):
        serializer = FootballFieldSerializers(data=request.data)
        current_user = get_authentication_user(request)
        if serializer.is_valid():
            # if the user is a field owner, assign current user  to the field owner
            if current_user.role == 'field_owner':
                serializer.save(owner=current_user)
            # if the user is an admin, check if the owner is provided
            elif current_user.role == 'admin':
                owner = serializer.validated_data.get('owner')
                if owner:
                    serializer.save()
                else:
                    return response.Response({'error': 'Field owner is required'},
                                             status=status.HTTP_400_BAD_REQUEST)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FootballCreateUpdate(views.APIView):
    permission_classes = [IsAdminAndFieldOwner]

    @swagger_auto_schema(
        operation_description="Update a football field",
        request_body=football_fields_schema_create,
        responses={
            200: football_fields_schema_response,
            400: 'Bad request',
            403: 'Forbidden',
            201: 'Created'
        }
    )
    def put(self, request, pk):
        football_field = get_object_or_404(FootballField, pk=pk)
        serializer = FootballFieldSerializersUpdate(football_field, data=request.data)
        # check if the user is the owner of the field
        current_user = get_authentication_user(request)
        if current_user.role == 'field_owner':
            if current_user != football_field.owner:
                return response.Response({'error': 'You are not the owner of this field'},
                                         status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            # if the user is a field owner, assign current user  to the field owner
            if current_user.role == 'field_owner':
                serializer.save(owner=current_user)
            # if the user is an admin, check if the owner is provided
            elif current_user.role == 'admin':
                if serializer.get_fields().get('owner'):
                    serializer.save()
                else:
                    return response.Response({'error': 'Field owner is required'},
                                             status=status.HTTP_400_BAD_REQUEST)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_distance(point: FootballField, point2):
    if point.latitude is None or point.longitude is None:
        return 0
    return math.sqrt((point.latitude - point2[0]) ** 2 + (point.longitude - point2[1]) ** 2)


def sort_by_closest(reference_point, fields):
    sorted_fields = sorted(fields, key=lambda field: calculate_distance(field, reference_point))
    return sorted_fields


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class AllFootballFields(views.APIView):
    permission_classes = [IsAdminAndUser, ]

    @swagger_auto_schema(
        operation_description="Get all football fields",
        responses={
            200: football_fields_schema_response,
            400: 'Bad request',
            403: 'Forbidden',
            201: 'Created'
        },
        manual_parameters=[
            openapi.Parameter(
                'start_time',
                openapi.IN_QUERY,
                description="Search query",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_time',
                openapi.IN_QUERY,
                description="Search query",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'latitude',
                openapi.IN_QUERY,
                description="Search query",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'longitude',
                openapi.IN_QUERY,
                description="Search query",
                type=openapi.TYPE_STRING
            ),
        ]

    )
    def get(self, request):
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        if latitude is not None and longitude is not None:
            if not (is_float(latitude) and is_float(longitude)):
                return response.Response({'error': 'Latitude and longitude must be float'},
                                         status=status.HTTP_400_BAD_REQUEST)
            football_fields = FootballField.objects.annotate_distance(latitude, longitude).all().order_by('distance')
        else:
            football_fields = FootballField.objects.all()

        if start_time is not None or end_time is not None:
            football_fields = football_fields.prefetch_related('reservations').exclude(
                Q(reservations__start_time__gte=start_time, reservations__end_time__lte=end_time) |
                Q(reservations__start_time__gt=start_time, reservations__start_time__lt=end_time) |
                Q(reservations__end_time__gt=start_time, reservations__end_time__lt=end_time))
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(football_fields, request)
        serializer = FootballFieldSerializers(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class DeleteFootballField(views.APIView):
    permission_classes = [IsAdminAndFieldOwner]


class CreateReservation(views.APIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(
        operation_description="Create a new reservation",
        request_body=reservation_create_schema,
        responses={
            400: 'Bad request',
            403: 'Forbidden',
            201: 'Created'
        }
    )
    def post(self, request):
        serializer = ReservationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteReservation(views.APIView):
    permission_classes = [IsAdminAndFieldOwner]

    @swagger_auto_schema(
        operation_description="Delete a reservation",
        manual_parameters=[
            openapi.Parameter(
                'field_id',
                openapi.IN_QUERY,
                description="Field ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
    )
    def delete(self, request, pk):
        filed_id = request.query_params.get('field_id', None)
        reservation = get_object_or_404(Reservation, pk=pk)
        current_user = get_authentication_user(request)
        if current_user.role == 'field_owner':
            for field in reservation.field.all():
                if current_user == field.owner:
                    reservation.field.remove(field)
                    break
            return response.Response(status=status.HTTP_204_NO_CONTENT)

        elif current_user.role == 'admin':
            if filed_id is None:
                return response.Response({'error': 'Field id is required'},
                                         status=status.HTTP_400_BAD_REQUEST)

            field = get_object_or_404(FootballField, pk=filed_id)
            reservation.field.remove(field)
            return response.Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return response.Response({'error': 'You are not the owner of this field'},
                                     status=status.HTTP_403_FORBIDDEN)


class ReservationList(views.APIView):
    permission_classes = [IsAdminAndFieldOwner]

    @swagger_auto_schema(
        operation_description="Get all reservations",
        responses={
            200: reservation_list_schema,
            400: 'Bad request',
            403: 'Forbidden',
        }
    )
    def get(self, request):
        current_user = get_authentication_user(request)
        if current_user.role == 'field_owner':
            reservations = Reservation.objects.prefetch_related('field').filter(field__owner=current_user).distinct()
        elif current_user.role == 'admin':
            reservations = Reservation.objects.all()
        else:
            return response.Response({'error': 'You are not the owner of this field'},
                                     status=status.HTTP_403_FORBIDDEN)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(reservations, request)
        serializer = ReservationSerializersResponse(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ListALLReservation(views.APIView):
    permission_classes = [IsAdminAndUser]

    def get(self, request):
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time is not None and end_time is not None:

            list_reservation = Reservation.objects.exclude(Q(start_time__gte=start_time, end_time__lte=end_time) |
                                                           Q(start_time__lt=start_time, start_time__gt=end_time) |
                                                           Q(end_time__lt=start_time, end_time__gt=end_time))

        else:
            list_reservation = Reservation.objects.all()

        return response.Response(ReservationSerializersResponse(list_reservation, many=True).data,
                                 status=status.HTTP_200_OK)
