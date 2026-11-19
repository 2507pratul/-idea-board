
import os
import psycopg

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Idea Board API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection URL must be provided through an environment variable.
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is required"
        )

    return psycopg.connect(DATABASE_URL)


@app.on_event("startup")
def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


class IdeaCreate(BaseModel):
    content: str


class IdeaUpdate(BaseModel):
    content: str


@app.get("/")
def home():
    return {"message": "Welcome to Idea Board API"}


@app.get("/api/ideas")
def get_ideas():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, content, created_at
            FROM ideas
            ORDER BY id DESC
        """).fetchall()

    return [
        {
            "id": row[0],
            "content": row[1],
            "created_at": row[2].isoformat()
        }
        for row in rows
    ]


@app.post("/api/ideas", status_code=201)
def create_idea(idea: IdeaCreate):
    content = idea.content.strip()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Idea content cannot be empty"
        )

    with get_connection() as conn:
        row = conn.execute("""
            INSERT INTO ideas (content)
            VALUES (%s)
            RETURNING id, content, created_at
        """, (content,)).fetchone()

    return {
        "id": row[0],
        "content": row[1],
        "created_at": row[2].isoformat()
    }


@app.put("/api/ideas/{idea_id}")
def update_idea(idea_id: int, idea: IdeaUpdate):
    content = idea.content.strip()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Idea content cannot be empty"
        )

    with get_connection() as conn:
        row = conn.execute("""
            UPDATE ideas
            SET content = %s
            WHERE id = %s
            RETURNING id, content, created_at
        """, (content, idea_id)).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Idea not found"
        )

    return {
        "id": row[0],
        "content": row[1],
        "created_at": row[2].isoformat()
    }


@app.delete("/api/ideas/{idea_id}")
def delete_idea(idea_id: int):
    with get_connection() as conn:
        row = conn.execute("""
            DELETE FROM ideas
            WHERE id = %s
            RETURNING id
        """, (idea_id,)).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Idea not found"
        )

    return {
        "message": "Idea deleted successfully",
        "id": row[0]
    }
