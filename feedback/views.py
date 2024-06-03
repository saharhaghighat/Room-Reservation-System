from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from feedback.models import Rating, Comment
from feedback.forms import CommentForm, RatingForm
from feedback.permissions import CommentOwnerOrAdminMixin, RatingOwnerOrAdminMixin


class RatingListView(ListView):
    model = Rating
    context_object_name = "ratings"
    template_name = "ratings/rating_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_id"] = self.kwargs["room_id"]
        return context

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return Rating.objects.filter(room_id=room_id)


class RatingCreateView(CreateView):
    model = Rating
    form_class = RatingForm
    template_name = "ratings/rating_form.html"

    def form_valid(self, form):
        form.instance.room_id = self.kwargs["room_id"]
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        room_id = self.kwargs["room_id"]
        return reverse_lazy("rating_list", kwargs={"room_id": room_id})


class RatingUpdateView(LoginRequiredMixin, RatingOwnerOrAdminMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    context_object_name = "rating"
    template_name = "ratings/rating_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        rating = self.object
        room_id = rating.room_id
        return (
            reverse_lazy("rating_list", kwargs={"room_id": room_id})
            + f"?rating_id={rating.id}"
        )


class RatingDeleteView(LoginRequiredMixin, RatingOwnerOrAdminMixin, DeleteView):
    model = Rating
    context_object_name = "rating"
    template_name = "ratings/rating_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room"] = self.object.room
        return context

    def get_success_url(self):
        room = self.get_object().room
        return reverse_lazy("rating_list", kwargs={"room_id": room.id})


class RoomCommentsView(ListView):
    model = Comment
    template_name = "comment/room_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return Comment.objects.filter(room_id=room_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_id"] = self.kwargs["room_id"]
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment/comment_form.html"

    def form_valid(self, form):
        form.instance.room_id = self.kwargs["room_id"]
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        room_id = self.kwargs["room_id"]
        return reverse_lazy("comments_list", kwargs={"room_id": room_id})


class CommentUpdateView(LoginRequiredMixin, CommentOwnerOrAdminMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment/comment_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        comment = self.object
        room_id = comment.room_id
        comment_id = comment.id
        return (
            reverse_lazy("comments_list", kwargs={"room_id": room_id})
            + f"?comment_id={comment_id}"
        )


class CommentDeleteView(LoginRequiredMixin, CommentOwnerOrAdminMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy("room-list")
    template_name = "comment/comment_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room"] = self.object.room
        return context

    def get_success_url(self):
        room = self.get_object().room
        return reverse_lazy("comments_list", kwargs={"room_id": room.id})
