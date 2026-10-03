from datetime import date
from django.core.management.base import BaseCommand
from movies.models import Movie

POSTERS = {
    "The Dark Knight": "https://images.unsplash.com/photo-1531259683007-016a7b628fc3?w=700",
    "Inception": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=700",
    "Interstellar": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=700",
    "Dune": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=700",
    "Oppenheimer": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=700",
    "The Matrix": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=700",
    "Whiplash": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=700",
    "The Social Network": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=700",
}

MOVIES = [
    ("The Dark Knight", 2008, 152, 9.0, 98, ["Action", "Crime", "Drama"], "Christopher Nolan", ["Jonathan Nolan", "Christopher Nolan"], ["Christian Bale", "Heath Ledger", "Aaron Eckhart"], "movie", True),
    ("Inception", 2010, 148, 8.8, 96, ["Action", "Sci-Fi", "Thriller"], "Christopher Nolan", ["Christopher Nolan"], ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Tom Hardy"], "movie", True),
    ("Interstellar", 2014, 169, 8.7, 94, ["Adventure", "Drama", "Sci-Fi"], "Christopher Nolan", ["Jonathan Nolan", "Christopher Nolan"], ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"], "movie", True),
    ("Dune", 2021, 155, 8.0, 92, ["Adventure", "Drama", "Sci-Fi"], "Denis Villeneuve", ["Jon Spaihts", "Denis Villeneuve"], ["Timothee Chalamet", "Zendaya", "Rebecca Ferguson"], "movie", True),
    ("Oppenheimer", 2023, 180, 8.6, 97, ["Biography", "Drama", "History"], "Christopher Nolan", ["Christopher Nolan"], ["Cillian Murphy", "Emily Blunt", "Matt Damon"], "movie", True),
    ("The Matrix", 1999, 136, 8.7, 90, ["Action", "Sci-Fi"], "Lana Wachowski", ["Lana Wachowski", "Lilly Wachowski"], ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"], "movie", False),
    ("The Social Network", 2010, 120, 7.8, 78, ["Biography", "Drama"], "David Fincher", ["Aaron Sorkin"], ["Jesse Eisenberg", "Andrew Garfield", "Justin Timberlake"], "movie", False),
    ("Whiplash", 2014, 107, 8.5, 85, ["Drama", "Music"], "Damien Chazelle", ["Damien Chazelle"], ["Miles Teller", "J.K. Simmons"], "movie", False),
    ("Stranger Things", 2016, 50, 8.7, 88, ["Drama", "Fantasy", "Mystery"], "The Duffer Brothers", ["The Duffer Brothers"], ["Millie Bobby Brown", "Finn Wolfhard", "Winona Ryder"], "series", False),
    ("Breaking Bad", 2008, 47, 9.5, 99, ["Crime", "Drama", "Thriller"], "Vince Gilligan", ["Vince Gilligan"], ["Bryan Cranston", "Aaron Paul", "Anna Gunn"], "series", True),
]


class Command(BaseCommand):
    help = "Seed CineScope with demo movies"

    def handle(self, *args, **kwargs):
        for title, year, duration, rating, popularity, genre, director, writers, stars, movie_type, featured in MOVIES:
            Movie.objects.update_or_create(
                title=title,
                defaults={
                    "year": year,
                    "duration": duration,
                    "rating": rating,
                    "popularity": popularity,
                    "genre": genre,
                    "description": f"A curated CineScope description for {title}, with memorable characters, strong storytelling and a world worth exploring.",
                    "director": director,
                    "writers": writers,
                    "stars": stars,
                    "type": movie_type,
                    "status": "published",
                    "reviews": [],
                    "poster_url": POSTERS.get(title, ""),
                    "backdrop_url": POSTERS.get(title, ""),
                    "language": "English",
                    "trailer_url": "",
                },
            )
        self.stdout.write(self.style.SUCCESS("CineScope sample movies loaded successfully."))
