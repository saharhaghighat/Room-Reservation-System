from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.urls import reverse_lazy

from reservation.models import Reservation
from reservation.forms import ReservationForm
from reservation.permissions import (
    TeamManagerMixin,
    AdminMixin,
    TeamMemberMixin,
    TeamMemberOrManagerOrAdminMixin,
    TeamManagerOrAdminMixin,
)


class ReservationCreateView(LoginRequiredMixin, TeamManagerOrAdminMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_form.html"
    success_url = reverse_lazy("reservation:reservation-list")

    def form_valid(self, form):
        if not self.request.user.is_team_manager:
            raise PermissionDenied(
                "You must be a team manager to create a reservation."
            )
        return super().form_valid(form)


class ReservationDetailView(
    LoginRequiredMixin, TeamMemberOrManagerOrAdminMixin, DetailView
):
    model = Reservation
    template_name = "reservation/reservation_detail.html"


class ReservationListView(LoginRequiredMixin, AdminMixin, ListView):
    model = Reservation
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservations"


class ReservationUpdateView(LoginRequiredMixin, TeamManagerOrAdminMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_form.html"
    success_url = reverse_lazy("reservation:reservation-list")


class ReservationDeleteView(LoginRequiredMixin, TeamManagerOrAdminMixin, DeleteView):
    model = Reservation
    template_name = "reservation/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservation:reservation-list")
