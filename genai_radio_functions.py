import os
import sqlite3
import random
from openai import OpenAI
client = OpenAI()

# ============================================================
# Initialize DB
# ============================================================
def init_db():
    conn = sqlite3.connect("genai_radio.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS podcasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            topics TEXT,
            filename TEXT
        )
    """)

    conn.commit()
    conn.close()

# ============================================================
# Replace fetch_live_news with OpenAI generator
# ===========================================================
def fetch_live_news(topic):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Give a short 3–4 sentence news-style update about this topic:
    {topic}

    Keep it factual, clear and easy to read.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # NEW SDK FORMAT
    return response.choices[0].message.content.strip()

# ============================================================
# MCQ Generator (unchanged)
# ============================================================
from nltk.tokenize import sent_tokenize

def generate_mcqs(sentences, n=5):
    mcqs = []
    random.shuffle(sentences)

    for s in sentences:
        if len(mcqs) >= n:
            break

        words = [w for w in s.split() if w.isalpha() and len(w) > 4]
        if not words:
            continue

        ans = random.choice(words)
        q = s.replace(ans, "_")

        fake = random.sample(["India", "Sports", "Science", "Tech", "Economy", "Health"], 3)
        opts = fake + [ans]
        random.shuffle(opts)

        mcqs.append({
            "question": q,
            "options": opts,
            "answer": ans
        })

    return mcqs