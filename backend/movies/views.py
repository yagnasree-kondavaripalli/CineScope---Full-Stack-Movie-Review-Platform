import json
from uuid import UUID

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Favorite, Watchlist
from .serializers import MovieSerializer, FavoriteSerializer, WatchlistSerializer


def movie_payload(movie):
    return MovieSerializer(movie).data


def movie_list_response(queryset):
    return JsonResponse([movie_payload(movie) for movie in queryset], safe=False, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_movies(request):
    include_upcoming = request.GET.get("includeUpcoming", request.GET.get("include_upcoming", "false")).lower() == "true"
    filter_keys = {"q", "genre", "year", "minRating", "maxRating", "minYear", "maxYear", "min_rating", "max_rating", "min_year", "max_year", "director", "writer", "type"}
    if filter_keys.intersection(request.GET.keys()):
        return search_movies(request)
    return movie_list_response(Movie.find_all(include_upcoming=include_upcoming))


@csrf_exempt
@require_http_methods(["GET"])
def get_movie_by_id(request, movie_id):
    try:
        movie_uuid = UUID(str(movie_id))
    except (ValueError, AttributeError, TypeError):
        return JsonResponse({"message": "Invalid movie ID format"}, status=400)
    try:
        movie = Movie.objects.get(id=movie_uuid)
    except Movie.DoesNotExist:
        return JsonResponse({"message": "Movie not found"}, status=404)
    return JsonResponse(movie_payload(movie), status=200)


@csrf_exempt
@require_http_methods(["GET"])
def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"message": "Search query required"}, status=400)
    return movie_list_response(Movie.search(query))


@csrf_exempt
@require_http_methods(["GET"])
def get_featured_movies(request):
    try:
        limit = int(request.GET.get("limit", "10"))
    except ValueError:
        limit = 10
    if not 1 <= limit <= 50:
        return JsonResponse({"message": "Limit must be between 1 and 50"}, status=400)
    return movie_list_response(Movie.get_featured(limit))


@csrf_exempt
@require_http_methods(["GET"])
def get_movies_by_type(request, movie_type):
    if movie_type not in {"movie", "series"}:
        return JsonResponse({"message": "Invalid type. Use movie or series."}, status=400)
    return movie_list_response(Movie.get_by_type(movie_type))


@csrf_exempt
@require_http_methods(["GET"])
def get_upcoming_movies(request):
    return movie_list_response(Movie.get_upcoming())


@csrf_exempt
@require_http_methods(["GET"])
def search_movies(request):
    p = request.GET
    qs = Movie.find_all(include_upcoming=False)

    q = p.get("q", "").strip()
    search_type = p.get("type", "all").strip().lower()
    if q:
        query = Q(title__icontains=q) | Q(description__icontains=q) | Q(director__icontains=q)
        if search_type == "title":
            query = Q(title__icontains=q)
        elif search_type in {"celebs", "celebrity", "star", "stars"}:
            query = Q(stars__icontains=q)
        elif search_type == "writer":
            query = Q(writers__icontains=q)
        qs = qs.filter(query)

    genre = p.get("genre")
    if genre:
        genres = [item.strip() for item in genre.split(",") if item.strip()]
        for item in genres:
            qs = qs.filter(genre__icontains=item)

    year = p.get("year")
    min_year = p.get("minYear") or p.get("min_year")
    max_year = p.get("maxYear") or p.get("max_year")
    min_rating = p.get("minRating") or p.get("min_rating")
    max_rating = p.get("maxRating") or p.get("max_rating")
    director = p.get("director")
    writer = p.get("writer")

    try:
        if year:
            qs = qs.filter(year=int(year))
        if min_year:
            qs = qs.filter(year__gte=int(min_year))
        if max_year:
            qs = qs.filter(year__lte=int(max_year))
        if min_rating:
            qs = qs.filter(rating__gte=float(min_rating))
        if max_rating:
            qs = qs.filter(rating__lte=float(max_rating))
    except ValueError:
        return JsonResponse({"message": "Invalid numeric filter"}, status=400)

    if director:
        qs = qs.filter(director__icontains=director)
    if writer:
        qs = qs.filter(writers__icontains=writer)

    return movie_list_response(qs.order_by("-rating", "-popularity", "-created_at"))


class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        p = self.request.query_params
        return Movie.find_all(include_upcoming=p.get("include_upcoming") == "true")


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = "id"
    lookup_url_kwarg = "movie_id"


class FeaturedMoviesView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.get_featured(12)


class TrendingMoviesView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.find_all().order_by("-popularity", "-rating")[:12]


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("movie")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        deleted, _ = Favorite.objects.filter(user=request.user, movie_id=pk).delete()
        return Response(status=204 if deleted else 404)


class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user).select_related("movie")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WatchlistDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        deleted, _ = Watchlist.objects.filter(user=request.user, movie_id=pk).delete()
        return Response(status=204 if deleted else 404)
