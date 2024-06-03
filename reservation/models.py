from datetime import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models

from account.models import Team
from room.models import Room, RoomSlot


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    date = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_reservation(room_id, team_id, start_time, end_time, date):
        reservation = Reservation.objects.create(
            room=room_id,
            team=team_id,
            start_time=start_time,
            end_time=end_time,
            date=date,
            created_at=datetime.now(),
        )
        return reservation

    # Read Reservation
    @staticmethod
    def get_reservation_by_id(reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            return reservation
        except Reservation.DoesNotExist:
            return Exception

    # Update operation
    @staticmethod
    def update_reservation(
            reservation_id,
            room_id=None,
            team_id=None,
            start_time=None,
            end_time=None,
            date=None,
    ):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            if room_id is not None:
                reservation.room_id = room_id
            if team_id is not None:
                reservation.team_id = team_id
            if start_time is not None:
                reservation.start_time = start_time
            if end_time is not None:
                reservation.end_time = end_time
            if date is not None:
                reservation.date = date
            reservation.save()
            return reservation
        except Reservation.DoesNotExist:
            return Exception

    # Delete Reservation
    @staticmethod
    def delete_reservation(reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()
            return True
        except Reservation.DoesNotExist:
            return False

    def __str__(self):
        return (
            f" Room ID: {self.room}, "
            f"Team ID: {self.team}, "
            f"Start Time: {self.start_time}, "
            f"End Time: {self.end_time},"
            f" Date: {self.date}, Created At: {self.created_at}"
        )

    def clean(self):
        # Ensure start_time is before end_time
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time.')

        # Ensure reservation date is in the future
        if self.date < timezone.now().date():
            raise ValidationError('Reservation date cannot be in the past.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

