# player/models.py
from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Audiobook, Chapter

User = get_user_model()

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progresses")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="progresses")
    position_seconds = models.PositiveIntegerField("Текущая позиция (сек)", default=0)
    is_finished = models.BooleanField("Прослушана до конца", default=False)
    last_listened_at = models.DateTimeField("Дата последнего прослушивания", auto_now=True)

    class Meta:
        verbose_name = "Прогресс прослушивания"
        verbose_name_plural = "Прогрессы"
        unique_together = ["user", "chapter"]

    def __str__(self):
        return f"{self.user.username} -> {self.chapter} ({self.position_seconds}с)"

    def get_percentage(self):
        """Возвращает процент прослушивания главы"""
        if self.chapter.duration == 0:
            return 0
        return round((self.position_seconds / self.chapter.duration) * 100, 1)

    def mark_as_finished(self):
        """Отметить главу как прослушанную"""
        self.position_seconds = self.chapter.duration
        self.is_finished = True
        self.save(update_fields=['position_seconds', 'is_finished', 'last_listened_at'])


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    title = models.CharField("Название плейлиста", max_length=150)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.username}: {self.title}"

    def get_total_duration(self):
        """Общая длительность плейлиста в секундах"""
        return sum(item.chapter.duration for item in self.items.all())

    def get_next_chapter(self, current_chapter):
        """Возвращает следующую главу в плейлисте"""
        current_item = self.items.filter(chapter=current_chapter).first()
        if current_item:
            next_item = self.items.filter(order__gt=current_item.order).order_by('order').first()
            return next_item.chapter if next_item else None
        return None


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="items")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="playlist_items")
    added_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Элемент плейлиста"
        verbose_name_plural = "Элементы плейлиста"
        unique_together = ["playlist", "chapter"]
        ordering = ["order"]

    def __str__(self):
        return f"{self.playlist.title} -> {self.chapter.title}"