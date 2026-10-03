import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export const api = axios.create({ baseURL, timeout: 10000 });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("cinescope_token");
  if (token) config.headers.Authorization = `Token ${token}`;
  return config;
});

export const getMovies = (params = {}) => api.get("/movies/", { params });
export const getMovie = (id) => api.get(`/movies/${id}/`);
export const getFeatured = () => api.get("/movies/featured/");
export const getTrending = () => api.get("/movies/trending/");
export const getUpcoming = () => api.get("/movies/upcoming/");
export const getReviews = (id) => api.get(`/movies/${id}/reviews/`);
export const addReview = (id, data) => api.post(`/movies/${id}/reviews/`, data);
export const login = (data) => api.post("/auth/login/", data);
export const register = (data) => api.post("/auth/register/", data);
export const getMe = () => api.get("/auth/me/");
export const getFavorites = () => api.get("/movies/favorites/");
export const addFavorite = (movie_id) => api.post("/movies/favorites/", { movie_id });
export const removeFavorite = (movie_id) => api.delete(`/movies/favorites/${movie_id}/`);
export const getWatchlist = () => api.get("/movies/watchlist/");
export const addWatchlist = (movie_id) => api.post("/movies/watchlist/", { movie_id });
export const removeWatchlist = (movie_id) => api.delete(`/movies/watchlist/${movie_id}/`);
