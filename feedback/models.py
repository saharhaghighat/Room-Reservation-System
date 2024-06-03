from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models, transaction

from room.models import Room

User = get_user_model()


class Comment(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_comment(room_id: int, author_id: int, content: str, reply_to_id: Optional[int] = None) -> "Comment":
        with transaction.atomic():
            comment = Comment(room_id=room_id, author_id=author_id, content=content, reply_to_id=reply_to_id)
            comment.save()
        return comment

    @staticmethod
    def get_comment(comment_id: int) -> Optional["Comment"]:
        try:
            return Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return None

    @staticmethod
    def update_comment(comment_id: int, content: str) -> Optional["Comment"]:
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return None

        comment.content = content
        comment.save()
        return comment

    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return False

        comment.delete()
        return True

    def __str__(self):
        return f"Comment by {self.author.username}: {self.content}"


class Rating(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.room} by {self.author} ({self.amount}/5)"

    @staticmethod
    def create_rating(room_id: int, author_id: int, amount: int) -> "Rating":
        with transaction.atomic():
            rating = Rating(room_id=room_id, author_id=author_id, amount=amount)
            rating.save()
        return rating

    @staticmethod
    def get_rating(rating_id: int) -> Optional["Rating"]:
        try:
            return Rating.objects.get(id=rating_id)
        except Rating.DoesNotExist:
            return None

    @staticmethod
    def update_rating(rating_id: int, amount: int) -> Optional["Rating"]:
        try:
            rating = Rating.objects.get(id=rating_id)
        except Rating.DoesNotExist:
            return None

        rating.amount = amount
        rating.save()
        return rating

    @staticmethod
    def delete_rating(rating_id: int) -> bool:
        try:
            rating = Rating.objects.get(id=rating_id)
        except Rating.DoesNotExist:
            return False

        rating.delete()
        return True
