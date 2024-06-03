from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, RoomSlot


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)


@admin.register(RoomSlot)
class RoomSlotAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_time', 'end_time', 'date', 'is_empty')
    list_filter = ('room', 'date', 'is_empty')
    search_fields = ('room__name',)
