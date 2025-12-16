# Hybrid Book Recommender System

A simple hybrid book recommendation app with a FastAPI backend and a static HTML/CSS/JS frontend. It supports viewing popular books, searching, and generating recommendations by book title. Basic auth (signup/login) is included.

## Features
- Popular books carousel and grid
- Search by title/author keywords
- Recommendations based on a selected book
- Signup and login with SQLite
- Docker Compose for easy local run

## Directory Structure
```
backend/              FastAPI app and dependencies
  app.py              API endpoints
  recommender.py      Popular/search/recommend logic backed by joblib assets
  requirements.txt    Python dependencies
  users.db            SQLite users database (auto-created)
books_data/           Data and models used by backend
  Books.csv, Ratings.csv, Users.csv
  popular_books.joblib, book_similarity.joblib, user_similarity.joblib, user_vs_books.joblib
home/                 Frontend Home page (HTML/CSS/JS)
popular/              Frontend Popular page
login/, signup/, profile/, notes/  Additional frontend pages
frontend/Dockerfile   Nginx image to serve static frontend
frontend/default.conf Nginx config serving Home page at root
backend/Dockerfile    Backend image
docker-compose.yml    Orchestration of backend and frontend
```

## Run Locally (without Docker)
Prereqs: Python 3.11+

1. Create and activate virtualenv
```
python3 -m venv .venv
source .venv/bin/activate
```
2. Install dependencies
```
pip install -r backend/requirements.txt
```
3. Start backend
```
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```
4. Serve frontend (from repo root)
```
python3 -m http.server 5500
```
5. Open the app
- Frontend: http://localhost:5500/home/home.html
- Backend health: http://localhost:8000/health

## Run with Docker
Prereqs: Docker Desktop

1. Build images
```
docker compose build
```
2. Start services
```
docker compose up -d
```
3. Verify
- Frontend: http://localhost:8080/
- Backend health: http://localhost:8000/health

4. Stop services
```
docker compose down
```

## API Reference
Base URL: `http://localhost:8000`

- Health
```
GET /health
```
- Popular Books
```
GET /books/popular?limit=20
```
- Search
```
GET /books/search?q=<query>&limit=10
```
- Recommend by Title
```
GET /recommend/by-title?title=<book title>&limit=8
```
- Signup
```
POST /auth/signup
Body: { first_name, last_name, age?, email, password }
```
- Login
```
POST /auth/login
Body: { email, password }
```

## Frontend Pages
- Home: `/home/home.html` (also served at site root `/` via nginx)
- Popular: `/popular/popular.html`
- Login: `/login/login.html`
- Signup: `/signup/signup.html`
- Profile: `/profile/profile.html`
- Notes: `/notes/notes.html`

## Notes
- The backend’s root path `/` returns 404 JSON by design; use the endpoints above.
- Nginx is configured to serve the Home page at `/` and to resolve assets with root‑relative paths.
- `users.db` is created automatically on first signup.