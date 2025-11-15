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
# ============================================================
def fetch_live_news(topic):
    """Generate topic-based explanation instead of live news."""
    prompt = f"""
    Create a friendly, engaging podcast narration about: {topic}.
    Requirements:
    - Do NOT mention dates or breaking news
    - Write as a general topic explanation (5–6 sentences)
    - Smooth, conversational, radio-host style
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()

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