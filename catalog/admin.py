from django.contrib import admin
from .models import Author, Genre, Audiobook, Chapter

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Audiobook)
class AudiobookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "total_duration", "created_at")
    list_filter = ("is_published", "genres", "author")
    search_fields = ("title", "author__name")
    inlines = [ChapterInline]
    actions = ["mark_published", "mark_unpublished"]

    def mark_published(self, request, queryset):
        queryset.update(is_published=True)
    mark_published.short_description = "Опубликовать выбранные книги"

    def mark_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    mark_unpublished.short_description = "Скрыть выбранные книги"

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "number", "audiobook", "duration")
    list_filter = ("audiobook",)
    search_fields = ("title", "audiobook__title")  # Обязательно для autocomplete_fields