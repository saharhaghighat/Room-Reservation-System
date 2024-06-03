from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from account.models import UserProfile


class AdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_admin


class OwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = get_object_or_404(UserProfile, pk=self.kwargs.get("pk"))
        return obj == self.request.user


class OwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return any(
            (
                AdminMixin.test_func(self),
                OwnerMixin.test_func(self),
            )
        )


class TeamManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_team_manager


class TeamMemberMixin(UserPassesTestMixin):
    def test_func(self):
        reservation = self.get_object()
        return self.request.user in reservation.team.members.all()


class TeamMemberOrManagerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return any(
            (
                TeamManagerMixin.test_func(self),
                TeamMemberMixin.test_func(self),
                AdminMixin.test_func(self),
            )
        )


class TeamManagerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return any(
            (
                TeamManagerMixin.test_func(self),
                AdminMixin.test_func(self),
            )
        )
