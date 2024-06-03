from typing import List, Optional

from django.contrib.auth.models import Group, AbstractUser
from django.db import models, transaction


class Team(Group):
    manager = models.ForeignKey(
        "account.UserProfile", related_name="managed_teams", on_delete=models.CASCADE
    )
    members = models.ManyToManyField("account.UserProfile", related_name="teams")

    @staticmethod
    def create_team(name: str, manager_id: int, member_ids: List[int]) -> "Team":
        with transaction.atomic():
            team = Team(name=name, manager_id=manager_id)
            team.save()

            members = UserProfile.objects.filter(id__in=member_ids)
            team.members.add(*members)

        return team

    @staticmethod
    def get_team(team_id: int) -> Optional["Team"]:
        try:
            return Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return None

    @staticmethod
    def update_team(
            team_id: int, name: Optional[str] = None, manager_id: Optional[int] = None
    ) -> Optional["Team"]:
        update_fields = {}
        if name is not None:
            update_fields["name"] = name

        if manager_id is not None:
            update_fields["manager_id"] = manager_id

        if not update_fields:
            return None

        updated_rows = Team.objects.filter(id=team_id).update(**update_fields)
        if updated_rows == 0:
            return None

        return Team.objects.get(id=team_id)

    @staticmethod
    def delete_team(team_id: int) -> bool:
        team = Team.get_team(team_id)
        if not team:
            return False

        team.delete()
        return True

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True,unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    # is_email_confirmed = models.BooleanField(default=False)
    is_team_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )

    def __str__(self):
        return self.username

    @staticmethod
    def create_user_profile(username, email, phone_number, team, is_team_manager, is_admin):
        user, created = AbstractUser.objects.get_or_create(username=username, email=email)
        profile = UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            team=team,
            is_team_manager=is_team_manager,
            is_admin=is_admin,
        )
        return profile

    @staticmethod
    def get_user_profile(username):
        try:
            profile = UserProfile.objects.get(user_username=username)

            return profile
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def update_user_profile(username, new_phone_number):
        try:
            profile = UserProfile.objects.get(user__username=username)
            profile.phone_number = new_phone_number
            profile.save()

            return profile
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def delete_user_profile(username):
        try:
            profile = UserProfile.objects.get(user__username=username)
            profile.delete()

            return True
        except UserProfile.DoesNotExist:
            return False


class OTP(models.Model):
    email = models.EmailField()
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email},{self.created},{self.code}'


class MobileOTP(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number},{self.created},{self.code}'
