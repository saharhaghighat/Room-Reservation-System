from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Reservation
from account.models import Team, UserProfile
from room.models import Room, RoomSlot
from datetime import datetime, timedelta


class ReservationModelTestCase(TestCase):
    def setUp(self):
        # Create a room
        self.room = Room.objects.create(name='Test Room', capacity=10)
        # Create a manager for the team
        self.manager = UserProfile.objects.create(username='manager', email='manager@example.com',
                                                  password='Password123!')
        # Create a team with the manager
        self.team = Team.objects.create(name='Test Team', manager=self.manager)

    def test_create_reservation(self):
        reservation = Reservation.create_reservation(
            room_id=self.room,
            team_id=self.team,
            start_time=datetime.now().time(),
            end_time=(datetime.now() + timedelta(hours=1)).time(),
            date=datetime.now().date()
        )
        self.assertIsNotNone(reservation.id)

    def test_get_reservation_by_id(self):
        reservation = Reservation.create_reservation(
            room_id=self.room,
            team_id=self.team,
            start_time=datetime.now().time(),
            end_time=(datetime.now() + timedelta(hours=1)).time(),
            date=datetime.now().date()
        )
        retrieved_reservation = Reservation.get_reservation_by_id(reservation.id)
        self.assertIsNotNone(retrieved_reservation)

    def test_update_reservation(self):
        reservation = Reservation.create_reservation(
            room_id=self.room,
            team_id=self.team,
            start_time=datetime.now().time(),
            end_time=(datetime.now() + timedelta(hours=1)).time(),
            date=datetime.now().date()
        )
        updated_room = Room.objects.create(name='Updated Room', capacity=5)
        updated_reservation = Reservation.update_reservation(
            reservation_id=reservation.id,
            room_id=updated_room.id
        )
        self.assertEqual(updated_reservation.room, updated_room)

    def test_delete_reservation(self):
        reservation = Reservation.create_reservation(
            room_id=self.room,
            team_id=self.team,
            start_time=datetime.now().time(),
            end_time=(datetime.now() + timedelta(hours=1)).time(),
            date=datetime.now().date()
        )
        Reservation.delete_reservation(reservation.id)
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())


class SignalTestCase(TestCase):
    def setUp(self):
        # Create a room
        self.room = Room.objects.create(name='Test Room', capacity=10)
        # Create a manager for the team
        self.manager = UserProfile.objects.create(username='manager', email='manager@example.com', password='password')
        # Create a team with the manager
        self.team = Team.objects.create(name='Test Team', manager=self.manager)

    def test_pre_save_reservation(self):
        Reservation(room=self.room, team=self.team, start_time='10:00:00', end_time='11:00:00', date='2024-03-15')
        self.assertRaises(ValidationError)

    def test_post_save_reservation(self):
        Reservation.objects.create(room=self.room, team=self.team, start_time='10:00:00',
                                   end_time='11:00:00', date='2024-03-15')
        room_slot = RoomSlot.objects.get(room=self.room, start_time='10:00:00', end_time='11:00:00', date='2024-03-15')
        self.assertFalse(room_slot.is_empty)

    @patch('reservation.signals.send_mail')
    def test_post_save_reservation_email(self, mock_send_mail):
        Reservation.objects.create(room=self.room, team=self.team, start_time='10:00:00',
                                   end_time='11:00:00', date='2024-03-15')
        self.assertTrue(mock_send_mail.called)

    def test_post_delete_reservation(self):
        reservation = Reservation.objects.create(room=self.room, team=self.team, start_time='10:00:00',
                                                 end_time='11:00:00', date='2024-03-15')
        reservation.delete()
        room_slot = RoomSlot.objects.get(room=self.room, start_time='10:00:00', end_time='11:00:00',
                                         date='2024-03-15')
        self.assertTrue(room_slot.is_empty)
