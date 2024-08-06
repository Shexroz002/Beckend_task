from django.urls import path
from .views import FootballCreateView, FootballCreateUpdate, AllFootballFields, ReservationList, CreateReservation, \
    DeleteReservation, ListALLReservation

app_name = 'football_fields'
urlpatterns = [
    path('create/', FootballCreateView.as_view(), name='create'),
    path('update/<int:pk>/', FootballCreateUpdate.as_view(), name='update'),
    path('all/', AllFootballFields.as_view(), name='all'),
    path('reservation/list/', ReservationList.as_view(), name='reservation'),
    path('reservation/create/', CreateReservation.as_view(), name='create_reservation'),
    path('reservation/delete/<int:pk>/', DeleteReservation.as_view(), name='delete_reservation'),
    path('search',ListALLReservation.as_view(),name="She")
]
