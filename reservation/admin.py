from django.contrib import admin

from reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'team', 'start_time', 'end_time', 'date', 'created_at')
    search_fields = ('room__name', 'team__name', 'date', 'start_time')
    list_filter = ('room', 'team', 'date')
