# urls.py
from django.urls import path
from .views import (
    RoomCreateView,
    RoomDetailView,
    RoomUpdateView,
    RoomDeleteView,
    RoomListView,
    reservations_for_month,
    room_calendar,
)

app_name = "room"

urlpatterns = [
    path("room/create/", RoomCreateView.as_view(), name="room-create"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),
    path("room/<int:pk>/update/", RoomUpdateView.as_view(), name="room-update"),
    path("room/<int:pk>/delete/", RoomDeleteView.as_view(), name="room-delete"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("room/<int:room_id>/calendar/", room_calendar, name="room_calendar"),
    path(
        "room/<int:room_id>/reservations-for-month/<int:year>/<int:month>/",
        reservations_for_month,
        name="reservations-for-day",
    ),
]
