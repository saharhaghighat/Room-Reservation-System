from django.urls import path
from .views import (
    ReservationCreateView,
    ReservationDetailView,
    ReservationUpdateView,
    ReservationDeleteView,
    ReservationListView,
)

app_name = "reservation"

urlpatterns = [
    path("reservation/", ReservationListView.as_view(), name="reservation-list"),
    path(
        "reservation/create/",
        ReservationCreateView.as_view(),
        name="reservation-create",
    ),
    path(
        "reservation/<int:pk>/",
        ReservationDetailView.as_view(),
        name="reservation-detail",
    ),
    path(
        "reservation/update/<int:pk>/",
        ReservationUpdateView.as_view(),
        name="reservation-update",
    ),
    path(
        "reservation/delete/<int:pk>/",
        ReservationDeleteView.as_view(),
        name="reservation-delete",
    ),
]
