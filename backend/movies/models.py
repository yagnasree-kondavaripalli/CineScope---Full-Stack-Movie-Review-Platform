import re
import uuid
from datetime import datetime

from django.db import models


class Movie(models.Model):
    TYPE_CHOICES = [("movie", "Movie"), ("series", "Series")]
    STATUS_CHOICES = [("upcoming", "Upcoming"), ("published", "Published")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(default=datetime.now().year)
    duration = models.PositiveIntegerField(default=120)
    rating = models.FloatField(default=0)
    popularity = models.PositiveIntegerField(default=0)
    genre = models.JSONField(default=list)
    description = models.TextField(blank=True)
    director = models.CharField(max_length=255, blank=True)
    writers = models.JSONField(default=list)
    stars = models.JSONField(default=list)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="movie")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="published")
    reviews = models.JSONField(default=list)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    language = models.CharField(max_length=50, default="English")
    trailer_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movies"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "type"]),
            models.Index(fields=["year"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["popularity"]),
        ]

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        self.description = self.description.strip()
        self.director = self.director.strip()
        super().save(*args, **kwargs)

    @classmethod
    def find_all(cls, include_upcoming=False):
        qs = cls.objects.all()
        if not include_upcoming:
            qs = qs.filter(status="published")
        return qs.order_by("-created_at")

    @classmethod
    def search(cls, query, include_upcoming=False):
        from django.db.models import Q
        qs = cls.find_all(include_upcoming=include_upcoming)
        q = re.escape((query or "").strip())
        if not q:
            return qs
        return qs.filter(
            Q(title__iregex=q) |
            Q(director__iregex=q) |
            Q(description__iregex=q)
        )

    @classmethod
    def get_featured(cls, limit=10):
        return cls.find_all().order_by("-popularity", "-rating")[:limit]

    @classmethod
    def get_by_type(cls, movie_type, include_upcoming=False):
        return cls.find_all(include_upcoming=include_upcoming).filter(type=movie_type)

    @classmethod
    def get_upcoming(cls):
        return cls.objects.filter(status="upcoming").order_by("year", "created_at")

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorite_entries")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "movie"], name="unique_favorite")]
        ordering = ["-created_at"]


class Watchlist(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="watchlist_entries")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlist_entries")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "movie"], name="unique_watchlist")]
        ordering = ["-created_at"]
