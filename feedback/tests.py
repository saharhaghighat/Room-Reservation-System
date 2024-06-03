from django.test import TestCase
from feedback.models import Comment, Rating
from room.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.

class CommentModelTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="room 1", capacity=10)
        self.author = User.objects.create(username="user 1", password="password 1")
        self.comment = Comment.objects.create(room = self.room, author = self.author, 
                content = "This is a test comment.")
       

    def test_comment_creation(self):
        self.assertEqual(self.comment.room, self.room)
        self.assertEqual(self.comment.author, self.author)
        self.assertEqual(self.comment.content, "This is a test comment.")

    def test_reply_to_field(self):
        reply_comment = Comment.objects.create(
            room=self.room,
            author=self.author,
            content='This is a reply to the test comment.',
            reply_to=self.comment,
        )
        self.assertEqual(reply_comment.reply_to, self.comment)


class RatingModelTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="room 1", capacity=10)
        self.author = User.objects.create(username="user 1", password="password 1")
        # self.amount = Rating.objects.create(room = self.room, author = self.author, 
        #         amount = "3")
       

    def test_rating_str(self):
        rating = Rating.objects.create(room=self.room, author=self.author, amount=3)
        expected_str = f"Rating for {self.room} by {self.author} (3/5)"
        self.assertEqual(str(rating), expected_str)
        self.assertIsNotNone(rating.created_at)