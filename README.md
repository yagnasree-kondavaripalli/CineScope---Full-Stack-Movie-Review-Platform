# CineScope — Full-Stack Movie Discovery Platform

CineScope is a portfolio-ready movie discovery application built with **React + Vite**, **Django + Django REST Framework**, and **SQLite**.

## Features

- Movie and series catalog
- Featured, trending and upcoming sections
- Search by title, description, director and stars
- Advanced filtering by genre, year range, rating range, director and writer
- Movie detail pages with UUID-based IDs
- Token authentication with registration/login/me endpoints
- Favorites and watchlist
- Reviews and 1–10 ratings
- Django Admin management
- Seed command with demo data
- API health endpoint
- Backend automated tests covering search and advanced filters
- Responsive React UI

## Project structure

```text
CineScope/
├── backend/
│   ├── config/
│   ├── movies/
│   │   ├── management/commands/seed_movies.py
│   │   ├── migrations/0001_initial.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests.py
│   ├── reviews/
│   ├── users/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env.example
└── README.md
```

## Windows setup

### 1. Backend

Open PowerShell in `CineScope\backend`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_movies
python manage.py createsuperuser
python manage.py runserver
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\venv\Scripts\Activate.ps1
```

### 2. Frontend

Open a **second terminal**:

```powershell
cd CineScope\frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally:

```text
http://localhost:5173
```

Backend:

```text
http://127.0.0.1:8000
```

API health:

```text
http://127.0.0.1:8000/api/health/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

## Important if you already have an older CineScope folder

Do **not** mix the old backend files with this version. Extract this project as a fresh folder. The included migration files are already created.

If you intentionally modify Django models later, then run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Main API endpoints

```text
GET  /api/movies/
GET  /api/movies/<uuid>/
GET  /api/movies/search/?q=inception
GET  /api/movies/advanced-search/?q=nolan&type=all
GET  /api/movies/featured/
GET  /api/movies/trending/
GET  /api/movies/upcoming/
GET  /api/movies/type/movie/
GET  /api/movies/type/series/
POST /api/auth/register/
POST /api/auth/login/
GET  /api/auth/me/
GET  /api/movies/favorites/
POST /api/movies/favorites/
DELETE /api/movies/favorites/<uuid>/
GET  /api/movies/watchlist/
POST /api/movies/watchlist/
DELETE /api/movies/watchlist/<uuid>/
GET  /api/movies/<uuid>/reviews/
POST /api/movies/<uuid>/reviews/
```

## Advanced search parameters

The backend supports both camelCase and snake_case for common numeric filters:

```text
q
 genre
 year
 minRating / min_rating
 maxRating / max_rating
 minYear / min_year
 maxYear / max_year
 director
 writer
 type=title|celebs|writer|all
```

Example:

```text
/api/movies/?genre=Sci-Fi&minRating=8.5&minYear=2000&maxYear=2025
```

## Testing

Run:

```powershell
python manage.py test
```

The included tests cover:

- listing movies
- title search
- celebrity search
- genre filtering
- rating + year filtering
- director + writer filtering
- UUID detail lookup
- invalid UUID handling
