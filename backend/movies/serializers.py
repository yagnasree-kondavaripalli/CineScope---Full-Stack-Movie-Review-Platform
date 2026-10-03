from rest_framework import serializers
from .models import Movie, Favorite, Watchlist


class MovieSerializer(serializers.ModelSerializer):
    _id = serializers.UUIDField(source="id", read_only=True)
    genre = serializers.JSONField()
    writers = serializers.JSONField()
    stars = serializers.JSONField()
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id", "_id", "title", "year", "duration", "rating", "popularity",
            "genre", "description", "director", "writers", "stars", "type", "status",
            "reviews", "poster_url", "backdrop_url", "language", "trailer_url",
            "createdAt", "updatedAt",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(source="movie", queryset=Movie.objects.all(), write_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "movie", "movie_id", "created_at"]


class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(source="movie", queryset=Movie.objects.all(), write_only=True)

    class Meta:
        model = Watchlist
        fields = ["id", "movie", "movie_id", "created_at"]
