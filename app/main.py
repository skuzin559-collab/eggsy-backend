from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("progress.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS save (
            id TEXT PRIMARY KEY,
            gems INTEGER
        );
    """)
    conn.commit()
    conn.close()

init_db()

class Progress(BaseModel):
    user_id: str
    gems: int

@app.get("/")
def root():
    return {"status": "Eggsyverse backend running"}

@app.post("/save")
def save_progress(p: Progress):
    conn = sqlite3.connect("progress.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO save (id, gems)
        VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET gems=excluded.gems
    """, (p.user_id, p.gems))
    conn.commit()
    conn.close()
    return {"status": "saved"}

@app.get("/load/{user_id}")
def load_progress(user_id: str):
    conn = sqlite3.connect("progress.db")
    c = conn.cursor()
    c.execute("SELECT gems FROM save WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return {"gems": row[0] if row else 0}
