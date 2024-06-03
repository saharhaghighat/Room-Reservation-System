from django.contrib.auth.mixins import UserPassesTestMixin


class TeamManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_team_manager


class AdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_admin


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
