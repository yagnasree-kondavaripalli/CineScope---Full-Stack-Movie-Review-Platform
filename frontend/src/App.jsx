import React, { useEffect, useState } from "react";
import {
  Link,
  Route,
  Routes,
  useNavigate,
  useParams
} from "react-router-dom";

import {
  addFavorite,
  addReview,
  addWatchlist,
  getFavorites,
  getFeatured,
  getMovie,
  getMovies,
  getReviews,
  getTrending,
  getWatchlist,
  login,
  register,
  removeFavorite,
  removeWatchlist
} from "./api";


function Nav() {
  const navigate = useNavigate();
  const logged = !!localStorage.getItem("cinescope_token");

  const logout = () => {
    localStorage.removeItem("cinescope_token");
    navigate("/");
    window.location.reload();
  };

  return (
    <nav className="nav">
      <Link className="brand" to="/">
        CineScope
      </Link>

      <div className="navlinks">
        <Link to="/">Home</Link>
        <Link to="/movies">Movies</Link>

        {logged ? (
          <>
            <Link to="/favorites">Favorites</Link>
            <Link to="/watchlist">Watchlist</Link>

            <button onClick={logout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}


function MovieCard({ movie }) {
  const genres = movie.genre || [];

  return (
    <Link className="card" to={`/movies/${movie.id}`}>
      <img
        src={
          movie.poster_url ||
          "https://placehold.co/400x600/191919/f5c518?text=Movie"
        }
        alt={movie.title}
      />

      <div className="cardbody">
        <h3>{movie.title}</h3>

        <p>
          {movie.release_date
            ? new Date(movie.release_date).getFullYear()
            : "N/A"}
          {" · "}
          {movie.duration || "N/A"} min
        </p>

        <span>
          ⭐ {movie.rating ?? "N/A"}
        </span>

        <small>
          {genres.join(" · ")}
        </small>
      </div>
    </Link>
  );
}


function Home() {
  const [featured, setFeatured] = useState([]);
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const loadHomeData = async () => {
      try {
        setLoading(true);
        setError("");

        const [featuredResponse, trendingResponse] =
          await Promise.all([
            getFeatured(),
            getTrending()
          ]);

        if (!mounted) return;

        setFeatured(featuredResponse.data || []);
        setTrending(trendingResponse.data || []);
      } catch (err) {
        console.error(err);

        if (mounted) {
          setError("Unable to load movies. Please check the backend server.");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadHomeData();

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <main>
      <section className="hero">
        <div>
          <p className="eyebrow">
            DISCOVER YOUR NEXT FAVORITE
          </p>

          <h1>
            Stories worth
            <br />
            <span>watching.</span>
          </h1>

          <p>
            Explore movies, discover new worlds, save your
            favorites and share your reviews.
          </p>

          <Link className="primary" to="/movies">
            Explore Movies
          </Link>
        </div>
      </section>

      {error && (
        <div className="empty">
          {error}
        </div>
      )}

      {loading ? (
        <div className="empty">
          Loading movies...
        </div>
      ) : (
        <>
          <MovieSection
            title="Featured"
            movies={featured}
          />

          <MovieSection
            title="Trending Now"
            movies={trending}
          />
        </>
      )}
    </main>
  );
}


function MovieSection({ title, movies }) {
  return (
    <section className="section">
      <div className="sectionhead">
        <h2>{title}</h2>

        <Link to="/movies">
          View all →
        </Link>
      </div>

      {movies.length > 0 ? (
        <div className="grid">
          {movies.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
            />
          ))}
        </div>
      ) : (
        <div className="empty">
          No movies available.
        </div>
      )}
    </section>
  );
}


function Movies() {
  const [movies, setMovies] = useState([]);
  const [search, setSearch] = useState("");
  const [genre, setGenre] = useState("");
  const [year, setYear] = useState("");
  const [minRating, setMinRating] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadMovies = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getMovies({
        q: search,
        genre: genre,
        year: year,
        minRating: minRating
      });

      setMovies(response.data || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load movies.");
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const loadInitialMovies = async () => {
      try {
        setLoading(true);

        const response = await getMovies({
          q: "",
          genre: "",
          year: "",
          minRating: ""
        });

        setMovies(response.data || []);
      } catch (err) {
        console.error(err);
        setError("Unable to load movies.");
      } finally {
        setLoading(false);
      }
    };

    loadInitialMovies();
  }, []);

  return (
    <main className="page">
      <div className="sectionhead">
        <h1>Explore Movies</h1>
      </div>

      <div className="filters">
        <input
          placeholder="Search title, director..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              loadMovies();
            }
          }}
        />

        <select
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        >
          <option value="">All genres</option>
          <option value="Action">Action</option>
          <option value="Drama">Drama</option>
          <option value="Sci-Fi">Sci-Fi</option>
          <option value="Thriller">Thriller</option>
          <option value="Comedy">Comedy</option>
          <option value="Adventure">Adventure</option>
        </select>

        <input
          type="number"
          placeholder="Year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />

        <input
          type="number"
          step="0.1"
          min="0"
          max="10"
          placeholder="Min rating"
          value={minRating}
          onChange={(e) => setMinRating(e.target.value)}
        />

        <button
          className="primary"
          onClick={loadMovies}
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {error && (
        <div className="empty">
          {error}
        </div>
      )}

      {loading ? (
        <div className="empty">
          Loading movies...
        </div>
      ) : movies.length > 0 ? (
        <div className="grid">
          {movies.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
            />
          ))}
        </div>
      ) : (
        <div className="empty">
          No movies found.
        </div>
      )}
    </main>
  );
}


function MovieDetails() {
  const { id } = useParams();

  const [movie, setMovie] = useState(null);
  const [reviews, setReviews] = useState([]);

  const [comment, setComment] = useState("");
  const [rating, setRating] = useState(10);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reviewLoading, setReviewLoading] = useState(false);

  const logged =
    !!localStorage.getItem("cinescope_token");

  useEffect(() => {
    let mounted = true;

    const loadMovieDetails = async () => {
      try {
        setLoading(true);
        setError("");

        const movieResponse = await getMovie(id);
        const reviewResponse = await getReviews(id);

        if (!mounted) return;

        setMovie(movieResponse.data);
        setReviews(reviewResponse.data || []);
      } catch (err) {
        console.error(err);

        if (mounted) {
          setError("Unable to load movie details.");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadMovieDetails();

    return () => {
      mounted = false;
    };
  }, [id]);

  const submitReview = async () => {
    if (!comment.trim()) {
      alert("Please write a review.");
      return;
    }

    try {
      setReviewLoading(true);

      await addReview(id, {
        rating: rating,
        comment: comment
      });

      setComment("");

      const response = await getReviews(id);
      setReviews(response.data || []);

      alert("Review posted successfully.");
    } catch (err) {
      console.error(err);
      alert("Unable to post review.");
    } finally {
      setReviewLoading(false);
    }
  };

  const handleFavorite = async () => {
    try {
      await addFavorite(movie.id);
      alert("Movie added to favorites.");
    } catch (err) {
      console.error(err);
      alert("Unable to add movie to favorites.");
    }
  };

  const handleWatchlist = async () => {
    try {
      await addWatchlist(movie.id);
      alert("Movie added to watchlist.");
    } catch (err) {
      console.error(err);
      alert("Unable to add movie to watchlist.");
    }
  };

  if (loading) {
    return (
      <main className="page">
        <div className="empty">
          Loading movie...
        </div>
      </main>
    );
  }

  if (error || !movie) {
    return (
      <main className="page">
        <div className="empty">
          {error || "Movie not found."}
        </div>
      </main>
    );
  }

  return (
    <main className="page">
      <div className="detail">
        <img
          src={
            movie.poster_url ||
            "https://placehold.co/500x750/191919/f5c518?text=Movie"
          }
          alt={movie.title}
        />

        <div>
          <p className="eyebrow">
            {(movie.genre || []).join(" · ")}
          </p>

          <h1>{movie.title}</h1>

          <p className="muted">
            {movie.release_date || "N/A"}
            {" · "}
            {movie.duration || "N/A"} min
            {" · "}
            {movie.language || "N/A"}
          </p>

          <h2>
            ⭐ {movie.rating ?? "N/A"}
          </h2>

          <p className="description">
            {movie.description}
          </p>

          <p>
            <b>Director:</b>{" "}
            {movie.director || "N/A"}
          </p>

          <p>
            <b>Cast:</b>{" "}
            {(movie.stars || []).join(", ") || "N/A"}
          </p>

          {logged && (
            <div className="actions">
              <button onClick={handleFavorite}>
                ♡ Add Favorite
              </button>

              <button onClick={handleWatchlist}>
                ＋ Watchlist
              </button>
            </div>
          )}
        </div>
      </div>

      <section className="reviewbox">
        <h2>Reviews</h2>

        {reviews.length > 0 ? (
          reviews.map((review) => (
            <div
              className="review"
              key={review.id}
            >
              <b>
                {review.username || "User"}
              </b>

              {" · "}

              ⭐ {review.rating}

              <p>
                {review.comment}
              </p>
            </div>
          ))
        ) : (
          <p className="muted">
            No reviews yet. Be the first to review this movie.
          </p>
        )}

        {logged && (
          <div className="reviewform">
            <select
              value={rating}
              onChange={(e) =>
                setRating(Number(e.target.value))
              }
            >
              {Array.from(
                { length: 10 },
                (_, index) => (
                  <option
                    key={index}
                    value={index + 1}
                  >
                    {index + 1}/10
                  </option>
                )
              )}
            </select>

            <textarea
              placeholder="Write a review..."
              value={comment}
              onChange={(e) =>
                setComment(e.target.value)
              }
            />

            <button
              className="primary"
              onClick={submitReview}
              disabled={reviewLoading}
            >
              {reviewLoading
                ? "Posting..."
                : "Post Review"}
            </button>
          </div>
        )}
      </section>
    </main>
  );
}


function Auth({ mode }) {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: ""
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");

      let response;

      if (mode === "login") {
        response = await login({
          username: form.username,
          password: form.password
        });
      } else {
        response = await register({
          username: form.username,
          email: form.email,
          password: form.password
        });
      }

      localStorage.setItem(
        "cinescope_token",
        response.data.token
      );

      navigate("/");
      window.location.reload();
    } catch (err) {
      console.error(err);

      setError(
        err?.response?.data?.detail ||
        err?.response?.data?.error ||
        "Authentication failed. Please check your details."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth">
      <form
        className="panel"
        onSubmit={submit}
      >
        <h1>
          {mode === "login"
            ? "Welcome back"
            : "Create account"}
        </h1>

        {error && (
          <div className="empty">
            {error}
          </div>
        )}

        <input
          placeholder="Username"
          required
          value={form.username}
          onChange={(e) =>
            setForm({
              ...form,
              username: e.target.value
            })
          }
        />

        {mode === "register" && (
          <input
            placeholder="Email"
            type="email"
            required
            value={form.email}
            onChange={(e) =>
              setForm({
                ...form,
                email: e.target.value
              })
            }
          />
        )}

        <input
          placeholder="Password"
          type="password"
          required
          value={form.password}
          onChange={(e) =>
            setForm({
              ...form,
              password: e.target.value
            })
          }
        />

        <button
          className="primary"
          disabled={loading}
        >
          {loading
            ? "Please wait..."
            : mode === "login"
            ? "Login"
            : "Register"}
        </button>

        <p>
          {mode === "login" ? (
            <>
              Don't have an account?{" "}
              <Link to="/register">
                Register
              </Link>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <Link to="/login">
                Login
              </Link>
            </>
          )}
        </p>
      </form>
    </main>
  );
}


function Saved({ type }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadSavedMovies = async () => {
    try {
      setLoading(true);
      setError("");

      let response;

      if (type === "favorites") {
        response = await getFavorites();
      } else {
        response = await getWatchlist();
      }

      setItems(response.data || []);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to load your saved movies."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSavedMovies();
  }, [type]);

  const remove = async (movieId) => {
    try {
      if (type === "favorites") {
        await removeFavorite(movieId);
      } else {
        await removeWatchlist(movieId);
      }

      await loadSavedMovies();
    } catch (err) {
      console.error(err);
      alert("Unable to remove movie.");
    }
  };

  return (
    <main className="page">
      <h1>
        {type === "favorites"
          ? "Your Favorites"
          : "Your Watchlist"}
      </h1>

      {error && (
        <div className="empty">
          {error}
        </div>
      )}

      {loading ? (
        <div className="empty">
          Loading...
        </div>
      ) : items.length > 0 ? (
        <div className="grid">
          {items.map((item) => (
            <div key={item.id}>
              <MovieCard movie={item.movie} />

              <button
                className="danger"
                onClick={() =>
                  remove(item.movie.id)
                }
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty">
          {type === "favorites"
            ? "You have no favorite movies yet."
            : "Your watchlist is empty."}
        </div>
      )}
    </main>
  );
}


export default function App() {
  return (
    <>
      <Nav />

      <Routes>
        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/movies"
          element={<Movies />}
        />

        <Route
          path="/movies/:id"
          element={<MovieDetails />}
        />

        <Route
          path="/login"
          element={<Auth mode="login" />}
        />

        <Route
          path="/register"
          element={<Auth mode="register" />}
        />

        <Route
          path="/favorites"
          element={<Saved type="favorites" />}
        />

        <Route
          path="/watchlist"
          element={<Saved type="watchlist" />}
        />
      </Routes>

      <footer>
        CineScope · Built with React + Django
      </footer>
    </>
  );
}