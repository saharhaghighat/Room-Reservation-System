from django.urls import path
from feedback.views import (
    RatingListView,
    RatingCreateView,
    RatingDeleteView,
    RatingUpdateView,
    CommentUpdateView,
    CommentCreateView,
    RoomCommentsView,
    CommentDeleteView,
)

urlpatterns = [
    path("ratings/<int:room_id>/", RatingListView.as_view(), name="rating_list"),
    path(
        "ratings/create/<int:room_id>/",
        RatingCreateView.as_view(),
        name="rating_create",
    ),
    path("ratings/<int:pk>/update/", RatingUpdateView.as_view(), name="rating_update"),
    path("ratings/<int:pk>/delete/", RatingDeleteView.as_view(), name="rating_delete"),
    path(
        "comments/create/<int:room_id>",
        CommentCreateView.as_view(),
        name="create-comment",
    ),
    path("comments/<int:room_id>/", RoomCommentsView.as_view(), name="comments_list"),
    path(
        "comments/<int:pk>/update", CommentUpdateView.as_view(), name="update-comment"
    ),
    path(
        "comments/<int:pk>/delete", CommentDeleteView.as_view(), name="delete-comment"
    ),
]
