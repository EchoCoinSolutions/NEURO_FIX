import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sentence_transformers import SentenceTransformer, util
from typing import List
from functools import lru_cache
import os, sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change_this_in_env")
model = SentenceTransformer("all-MiniLM-L6-v2")

conn = sqlite3.connect("phrases.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS phrases (
    phrase TEXT PRIMARY KEY,
    category TEXT,
    is_sovereign INTEGER DEFAULT 0
)
""")
conn.commit()

unmatched_phrases = []

@lru_cache(maxsize=1000)
def get_embedding(text: str):
    return model.encode(text, convert_to_tensor=True)

def find_best_match(input_phrase: str, threshold=0.7):
    cursor.execute("SELECT phrase FROM phrases WHERE is_sovereign = 0")
    phrases = [row[0] for row in cursor.fetchall()]
    if not phrases:
        return None, 0.0
    input_vec = get_embedding(input_phrase)
    best_score = 0.0
    best_phrase = None
    for phrase in phrases:
        score = float(util.pytorch_cos_sim(input_vec, get_embedding(phrase)))
        if score > best_score:
            best_score = score
            best_phrase = phrase
    if best_score >= threshold:
        cursor.execute("SELECT category FROM phrases WHERE phrase=?", (best_phrase,))
        result = cursor.fetchone()
        return result[0] if result else None, best_score
    return None, best_score

@app.post("/match")
async def match_phrase(phrase: str = Form(...)):
    cursor.execute("SELECT category, is_sovereign FROM phrases WHERE phrase=?", (phrase,))
    row = cursor.fetchone()
    if row:
        category, is_sovereign = row
        return {"category": "sovereign" if is_sovereign else category, "confidence": 1.0}
    category, score = find_best_match(phrase)
    if category:
        return {"category": category, "confidence": score}
    unmatched_phrases.append(phrase)
    return {"category": "unmatched", "confidence": 0.0}

@app.get("/admin", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/admin")
async def admin_check(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        return RedirectResponse(url="/review", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect password"})

@app.get("/review", response_class=HTMLResponse)
async def review(request: Request):
    cursor.execute("SELECT phrase, category FROM phrases WHERE is_sovereign=0")
    approved = cursor.fetchall()
    cursor.execute("SELECT phrase FROM phrases WHERE is_sovereign=1")
    sovereign = [row[0] for row in cursor.fetchall()]
    return templates.TemplateResponse("review.html", {
        "request": request,
        "unmatched": unmatched_phrases[-50:],
        "approved": approved,
        "sovereign": sovereign
    })

@app.post("/approve")
async def approve_phrase(phrase: str = Form(...), category: str = Form(...)):
    cursor.execute("INSERT OR REPLACE INTO phrases (phrase, category, is_sovereign) VALUES (?, ?, 0)", (phrase, category))
    conn.commit()
    if phrase in unmatched_phrases:
        unmatched_phrases.remove(phrase)
    return RedirectResponse(url="/review", status_code=302)

@app.post("/sovereign")
async def mark_sovereign(phrase: str = Form(...)):
    cursor.execute("INSERT OR REPLACE INTO phrases (phrase, category, is_sovereign) VALUES (?, '', 1)", (phrase,))
    conn.commit()
    if phrase in unmatched_phrases:
        unmatched_phrases.remove(phrase)
    return RedirectResponse(url="/review", status_code=302)

@app.post("/delete")
async def delete_phrase(phrase: str = Form(...)):
    cursor.execute("DELETE FROM phrases WHERE phrase=?", (phrase,))
    conn.commit()
    return RedirectResponse(url="/review", status_code=302)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

