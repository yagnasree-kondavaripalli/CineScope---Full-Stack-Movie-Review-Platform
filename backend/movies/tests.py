import uuid
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Movie


class CineScopeMovieAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title="Inception",
            year=2010,
            duration=148,
            rating=8.8,
            popularity=96,
            genre=["Action", "Sci-Fi", "Thriller"],
            description="A dream-based thriller.",
            director="Christopher Nolan",
            writers=["Christopher Nolan"],
            stars=["Leonardo DiCaprio", "Tom Hardy"],
            type="movie",
            status="published",
        )
        self.other = Movie.objects.create(
            title="Dune",
            year=2021,
            duration=155,
            rating=8.0,
            popularity=92,
            genre=["Adventure", "Sci-Fi"],
            description="A desert epic.",
            director="Denis Villeneuve",
            writers=["Jon Spaihts"],
            stars=["Zendaya"],
            type="movie",
            status="published",
        )

    def test_get_all_movies(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_find_movies_by_title(self):
        response = self.client.get("/api/movies/search/", {"q": "Inception"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "Inception")

    def test_find_movies_by_celebrity(self):
        response = self.client.get("/api/movies/advanced-search/", {"q": "Zendaya", "type": "celebs"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_filter_by_genre(self):
        response = self.client.get("/api/movies/", {"genre": "Sci-Fi"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_filter_by_rating_and_year(self):
        response = self.client.get("/api/movies/", {"minRating": "8.5", "maxRating": "9.0", "minYear": "2000", "maxYear": "2015"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "Inception")

    def test_filter_by_director_and_writer_combined(self):
        response = self.client.get("/api/movies/", {"director": "Christopher", "writer": "Nolan"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_movie_by_id(self):
        response = self.client.get(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["_id"], str(self.movie.id))

    def test_invalid_movie_id(self):
        response = self.client.get("/api/movies/not-a-uuid/")
        self.assertEqual(response.status_code, 400)
