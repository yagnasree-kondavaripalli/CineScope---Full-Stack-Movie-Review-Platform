from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from movies.models import Movie


class MovieReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(movie_id=self.kwargs["movie_id"]).select_related("user", "movie")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, id=self.kwargs["movie_id"])
        serializer.save(user=self.request.user, movie=movie)
