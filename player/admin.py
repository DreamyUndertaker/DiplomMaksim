from django.contrib import admin
from .models import UserProgress, Playlist, PlaylistItem

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "chapter", "position_seconds", "is_finished", "last_listened_at")
    list_filter = ("is_finished", "chapter__audiobook")
    search_fields = ("user__username", "chapter__title")

class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 1
    autocomplete_fields = ["chapter"]

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")
    search_fields = ("title", "user__username")
    inlines = [PlaylistItemInline]