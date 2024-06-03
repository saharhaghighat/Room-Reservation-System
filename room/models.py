from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()

    @staticmethod
    def create_room(name, capacity):
        room = Room.objects.create(name=name, capacity=capacity)
        return room

    @staticmethod
    def get_room_by_id(room_id):
        try:
            room = Room.objects.get(pk=room_id)
            return room
        except Room.DoesNotExist:
            return None

    @staticmethod
    def get_all_rooms():
        rooms = Room.objects.all()
        return rooms

    @staticmethod
    def update_room(room_id, name=None, capacity=None):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None

        if name is not None:
            room.name = name
        if capacity is not None:
            room.capacity = capacity

        room.save()
        return room

    @staticmethod
    def delete_room(room_id):
        room = Room.get_room_by_id(room_id)
        if room:
            room.delete()
            return True
        return False

    def __str__(self):
        return f"{self.name} has {self.capacity} capacity"


class RoomSlot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    date = models.DateField(null=False)
    is_empty = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.room.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')}, Is Empty: {self.is_empty}"

