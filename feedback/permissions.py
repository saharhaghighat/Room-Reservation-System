from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from feedback.models import Rating, Comment


class AdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_admin


class CommentOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        return obj == self.request.user


class CommentOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return any(
            (
                AdminMixin.test_func(self),
                CommentOwnerMixin.test_func(self),
            )
        )


class RatingOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = get_object_or_404(Rating, pk=self.kwargs.get("pk"))
        return obj == self.request.user


class RatingOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return any(
            (
                AdminMixin.test_func(self),
                CommentOwnerMixin.test_func(self),
            )
        )
