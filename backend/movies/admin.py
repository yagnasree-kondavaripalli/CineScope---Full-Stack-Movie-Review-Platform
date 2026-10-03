from django.contrib import admin
from .models import Movie, Favorite, Watchlist


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "type", "status", "rating", "popularity", "director")
    list_filter = ("type", "status", "year")
    search_fields = ("title", "director", "description")
    ordering = ("-popularity", "-rating")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "created_at")
    search_fields = ("user__username", "movie__title")


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "created_at")
    search_fields = ("user__username", "movie__title")
