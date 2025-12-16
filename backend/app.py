import os
import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from . import recommender

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            email TEXT UNIQUE,
            password_hash TEXT
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.mount("/home", StaticFiles(directory=os.path.join(BASE_DIR, "home"), html=True), name="home")
app.mount("/popular", StaticFiles(directory=os.path.join(BASE_DIR, "popular"), html=True), name="popular")
app.mount("/login", StaticFiles(directory=os.path.join(BASE_DIR, "login"), html=True), name="login")
app.mount("/signup", StaticFiles(directory=os.path.join(BASE_DIR, "signup"), html=True), name="signup")
app.mount("/profile", StaticFiles(directory=os.path.join(BASE_DIR, "profile"), html=True), name="profile")
app.mount("/notes", StaticFiles(directory=os.path.join(BASE_DIR, "notes"), html=True), name="notes")

class SignupBody(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int]
    email: EmailStr
    password: str

class LoginBody(BaseModel):
    email: EmailStr
    password: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return RedirectResponse(url="/home/home.html")

@app.get("/books/popular")
def books_popular(limit: int = 20):
    return recommender.get_popular(limit)

@app.get("/books/search")
def books_search(q: str, limit: int = 20):
    return recommender.search_books(q, limit)

@app.get("/recommend/by-title")
def recommend_by_title(title: str, limit: int = 10):
    return recommender.recommend_by_title(title, limit)

@app.post("/auth/signup")
def signup(body: SignupBody):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = ?", (body.email,))
    exists = cur.fetchone()
    if exists:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = pwd_context.hash(body.password)
    cur.execute(
        "INSERT INTO users (first_name, last_name, age, email, password_hash) VALUES (?, ?, ?, ?, ?)",
        (body.first_name, body.last_name, body.age or 0, body.email, password_hash)
    )
    conn.commit()
    conn.close()
    return {"ok": True}

@app.post("/auth/login")
def login(body: LoginBody):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, first_name, last_name, age, email FROM users WHERE email = ?", (body.email,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id, password_hash, first_name, last_name, age, email = row
    if not pwd_context.verify(body.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": user_id, "first_name": first_name, "last_name": last_name, "age": age, "email": email}