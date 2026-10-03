from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_movies, name="get_all_movies"),
    path("search/", views.search, name="search"),
    path("advanced-search/", views.search_movies, name="search_movies"),
    path("filter/", views.search_movies, name="filter_movies"),
    path("featured/", views.get_featured_movies, name="get_featured_movies"),
    path("trending/", views.TrendingMoviesView.as_view(), name="trending_movies"),
    path("upcoming/", views.get_upcoming_movies, name="get_upcoming_movies"),
    path("type/<str:movie_type>/", views.get_movies_by_type, name="get_movies_by_type"),
    path("favorites/", views.FavoriteListCreateView.as_view(), name="favorites"),
    path("favorites/<uuid:pk>/", views.FavoriteDeleteView.as_view(), name="favorite_delete"),
    path("watchlist/", views.WatchlistListCreateView.as_view(), name="watchlist"),
    path("watchlist/<uuid:pk>/", views.WatchlistDeleteView.as_view(), name="watchlist_delete"),
    path("<str:movie_id>/", views.get_movie_by_id, name="get_movie_by_id"),
]
