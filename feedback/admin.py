from django.contrib import admin

from feedback.models import Comment, Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "author", "amount", "created_at")
    list_filter = ("amount", "created_at", "room", "author")
    search_fields = ("room__name", "author__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "author", "reply_to", "short_content", "created_at")
    list_filter = ("created_at", "room", "author")
    search_fields = ("content", "author__username", "room__name")

    @admin.display(description="Content")
    def short_content(self, obj):
        return obj.content[:50]
