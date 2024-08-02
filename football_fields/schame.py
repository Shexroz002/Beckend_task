from drf_yasg import openapi
from users.schame import customer_schema

image_list = openapi.Schema(
    title='ImageList',
    type=openapi.TYPE_OBJECT,
    properties={
        'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image of the football field'),
    }
)
image_file = openapi.Schema(
    title='ImageFile',
    type=openapi.TYPE_OBJECT,
    properties={
        'image': openapi.Schema(type=openapi.TYPE_FILE, description='Image of the football field'),
    }
)
football_fields_schema_response = openapi.Schema(
    title='FootballFields',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the football field'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the football field'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the football field'),
        'contact': openapi.Schema(type=openapi.TYPE_STRING, description='Contact of the football field', ),
        'price_per_hour': openapi.Schema(type=openapi.TYPE_NUMBER, description='Price per hour of the football field'),
        'owner': customer_schema,
        'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Latitude of the football field'),
        'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Longitude of the football field'),
        'images': openapi.Schema(type=openapi.TYPE_ARRAY, items=image_list, description='Images of the football field'),
    }
)

football_fields_schema_create = openapi.Schema(
    title='FootballFields',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the football field'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the football field'),
        'contact': openapi.Schema(type=openapi.TYPE_STRING, description='Contact of the football field', ),
        'price_per_hour': openapi.Schema(type=openapi.TYPE_NUMBER, description='Price per hour of the football field'),
        'owner': openapi.Schema(type=openapi.TYPE_INTEGER, description='Owner of the football field'),
        'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Latitude of the football field'),
        'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Longitude of the football field'),
        'images': openapi.Schema(type=openapi.TYPE_FILE, description='Images of the football field'),
    }
)

reservation_create_schema = openapi.Schema(
    title='Reservation',
    type=openapi.TYPE_OBJECT,
    properties={
        'field': openapi.Schema(type=openapi.TYPE_INTEGER, description='Field ID'),
        'date': openapi.Schema(type=openapi.TYPE_STRING, description='Date of reservation'),
        'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='Start time of reservation'),
        'end_time': openapi.Schema(type=openapi.TYPE_STRING, description='End time of reservation'),
    }
)
reservation_foot_ball_schema = openapi.Schema(
    title='Reservation',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the reservation'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Field ID')
    }
)

reservation_list_schema = openapi.Schema(
    title='Reservation',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the reservation'),
        'field': openapi.Schema(type=openapi.TYPE_INTEGER, description='Field ID'),
        'date': openapi.Schema(type=openapi.TYPE_STRING, description='Date of reservation'),
        'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='Start time of reservation'),
        'end_time': openapi.Schema(type=openapi.TYPE_STRING, description='End time of reservation'),
    }
)