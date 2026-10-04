import re

SKILLS = {"python", "kubernetes", "terraform", "gcp", "fastapi"}


def extract(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text is empty")
    tokens = set(re.findall(r"[a-z0-9+.#]+", text.lower()))
    found = sorted(skill for skill in SKILLS if skill in tokens or skill in text.lower())
    return {"skills": found, "count": len(found)}
