# catalog/models.py
from django.db import models
from django.utils.text import slugify

class Author(models.Model):
    name = models.CharField("Имя автора", max_length=150, unique=True)
    bio = models.TextField("Биография", blank=True)
    photo = models.ImageField("Фото автора", upload_to="authors/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=100, unique=True)
    slug = models.SlugField("Слаг", unique=True, max_length=100)
    description = models.TextField("Описание жанра", blank=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Audiobook(models.Model):
    title = models.CharField("Название книги", max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор", related_name="books")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", related_name="books", blank=True)
    cover = models.ImageField("Обложка", upload_to="covers/", default="covers/default.jpg")
    description = models.TextField("Описание", blank=True)
    publication_year = models.PositiveSmallIntegerField("Год публикации", null=True, blank=True)
    total_duration = models.PositiveIntegerField("Общая длительность (сек)", default=0, editable=False)
    is_published = models.BooleanField("Опубликована", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Аудиокнига"
        verbose_name_plural = "Аудиокниги"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.author.name})"

    def update_duration(self):
        self.total_duration = self.chapters.aggregate(models.Sum("duration"))["duration__sum"] or 0
        self.save(update_fields=["total_duration", "updated_at"])


class Chapter(models.Model):
    audiobook = models.ForeignKey(Audiobook, on_delete=models.CASCADE, verbose_name="Книга", related_name="chapters")
    title = models.CharField("Название главы", max_length=255)
    number = models.PositiveSmallIntegerField("Номер главы")
    audio_file = models.FileField("Аудиофайл", upload_to="chapters/")
    duration = models.PositiveIntegerField("Длительность (сек)", default=0)

    class Meta:
        verbose_name = "Глава"
        verbose_name_plural = "Главы"
        unique_together = ["audiobook", "number"]
        ordering = ["number"]

    def __str__(self):
        return f"{self.audiobook.title} - Глава {self.number}: {self.title}"