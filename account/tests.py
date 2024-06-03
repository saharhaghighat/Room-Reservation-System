from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import Team, UserProfile

# Create your tests here.

User = get_user_model()

class TestTeamModel(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username="manager", email="manager1@email.com", password="pass1")

        self.team = Team.objects.create(name="name1", manager=self.manager)

        self.member1 = User.objects.create(username="member1", email="member1@email.com", password="pass2")
        self.member2 = User.objects.create(username="member2", email="member2@email.com", password="pass3")
        
        self.team.members.add(self.member1, self.member2)

    def test_team_creation(self):
        self.assertEqual(self.team.name, "name1")
        self.assertEqual(self.team.manager, self.manager)

    def test_team_members(self):
        self.assertIn(self.member1, self.team.members.all())
        self.assertIn(self.member2, self.team.members.all())

    def test_manager_managed_teams(self):
        self.assertIn(self.team, self.manager.managed_teams.all())

    def test_member_teams(self):
        self.assertIn(self.team, self.member1.teams.all())
        self.assertIn(self.team, self.member2.teams.all())