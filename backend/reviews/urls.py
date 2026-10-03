from django.urls import path
from .views import MovieReviewListCreateView

urlpatterns = [path("movies/<uuid:movie_id>/reviews/", MovieReviewListCreateView.as_view(), name="movie_reviews")]
