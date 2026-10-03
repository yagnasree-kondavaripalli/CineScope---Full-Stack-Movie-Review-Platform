# Generated for CineScope
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency("auth.User"),
    ]

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("year", models.PositiveIntegerField(default=2026)),
                ("duration", models.PositiveIntegerField(default=120)),
                ("rating", models.FloatField(default=0)),
                ("popularity", models.PositiveIntegerField(default=0)),
                ("genre", models.JSONField(default=list)),
                ("description", models.TextField(blank=True)),
                ("director", models.CharField(blank=True, max_length=255)),
                ("writers", models.JSONField(default=list)),
                ("stars", models.JSONField(default=list)),
                ("type", models.CharField(choices=[("movie", "Movie"), ("series", "Series")], default="movie", max_length=10)),
                ("status", models.CharField(choices=[("upcoming", "Upcoming"), ("published", "Published")], default="published", max_length=10)),
                ("reviews", models.JSONField(default=list)),
                ("poster_url", models.URLField(blank=True)),
                ("backdrop_url", models.URLField(blank=True)),
                ("language", models.CharField(default="English", max_length=50)),
                ("trailer_url", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "movies", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorite_entries", to="movies.movie")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="auth.user")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Watchlist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="watchlist_entries", to="movies.movie")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="watchlist_entries", to="auth.user")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(fields=("user", "movie"), name="unique_favorite"),
        ),
        migrations.AddConstraint(
            model_name="watchlist",
            constraint=models.UniqueConstraint(fields=("user", "movie"), name="unique_watchlist"),
        ),
        migrations.AddIndex(model_name="movie", index=models.Index(fields=["status", "type"], name="movies_statu_9d3b3b_idx")),
        migrations.AddIndex(model_name="movie", index=models.Index(fields=["year"], name="movies_year_5d8a3a_idx")),
        migrations.AddIndex(model_name="movie", index=models.Index(fields=["rating"], name="movies_ratin_7fdb61_idx")),
        migrations.AddIndex(model_name="movie", index=models.Index(fields=["popularity"], name="movies_popul_6a6d6b_idx")),
    ]
