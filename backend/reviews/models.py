from django.contrib.auth.models import User
from django.db import models
from movies.models import Movie


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="review_objects")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["user", "movie"], name="unique_user_movie_review")]

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
