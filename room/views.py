from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)

from room.permissions import AdminMixin
from room.models import Room
from reservation.models import Reservation
from django.http import JsonResponse
from reservation.models import Reservation
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta


class RoomCreateView(LoginRequiredMixin, AdminMixin, CreateView):
    model = Room
    fields = ["name", "capacity"]
    template_name = "room/room_form.html"
    success_url = reverse_lazy("room:room-list")


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = "room/room_detail.html"


class RoomUpdateView(LoginRequiredMixin, AdminMixin, UpdateView):
    model = Room
    fields = ["name", "capacity"]
    template_name = "room/room_form.html"
    success_url = reverse_lazy("room:room-list")


class RoomDeleteView(LoginRequiredMixin, AdminMixin, DeleteView):
    model = Room
    success_url = reverse_lazy("room:room-list")
    template_name = "room/room_confirm_delete.html"


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "room/room_list.html"
    context_object_name = "rooms"


def room_calendar(request, room_id):
    room_reservations = Reservation.objects.filter(room_id=room_id)
    return render(
        request, "room/room_calendar.html", {"reservations": room_reservations}
    )


def reservations_for_month(request, room_id, year, month):
    room = get_object_or_404(Room, pk=room_id)
    month_start = timezone.datetime(year, month, 1).date()
    month_end = (timezone.datetime(year, month, 1) + timedelta(days=32)).replace(
        day=1
    ) - timedelta(days=1)

    reservations = Reservation.objects.filter(
        room=room, date__range=[month_start, month_end]
    )

    events = []
    for reservation in reservations:
        start_datetime = timezone.datetime.combine(
            reservation.date, reservation.start_time
        )
        end_datetime = timezone.datetime.combine(reservation.date, reservation.end_time)
        event = {
            "id": reservation.id,
            "title": f"{reservation.team.name}",
            "start": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "date": reservation.date.strftime("%Y-%m-%d"),
        }
        events.append(event)

    return JsonResponse(events, safe=False)


## FOR RESERVATIONS IN A DAY

# def reservations_for_day(request, room_id, year, month, day):
#     room = get_object_or_404(Room, pk=room_id)
#     date = timezone.datetime(year, month, day).date()
#     reservations = Reservation.objects.filter(room=room, date=date)

#     events = []
#     for reservation in reservations:
#         start_datetime = timezone.datetime.combine(date, reservation.start_time)
#         end_datetime = timezone.datetime.combine(date, reservation.end_time)
#         event = {
#             'id': reservation.id,  # Include a unique identifier for each event
#             'start': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
#             'end': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
#             'title': f'{reservation.team.name} - {reservation.start_time.strftime("%I:%M %p")}-{reservation.end_time.strftime("%I:%M %p")}',
#             'date': date.strftime('%Y-%m-%d')  # Add the date field
#         }
#         events.append(event)

#     return JsonResponse(events, safe=False)
