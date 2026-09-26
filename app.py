import base64, json, logging, os
from functools import lru_cache

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from google import genai

load_dotenv()  # GEMINI_API_KEY (and optional GEMINI_MODEL) from .env; real env vars win
app = Flask(__name__, static_folder="static")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

PROMPT = """You are a scam-detection assistant for everyday people. Decide whether the input is a scam, suspicious, or safe. \
Quote the exact phrases that raise concern. Explain each in plain English with no jargon. Name any brand or agency being imitated. \
Use web search to check whether the sender, number, URL or wording matches known scams. \
Next steps must be safe (do not click, report to the right place, contact the real company through its official site). \
If it looks legitimate, say so and keep red_flags short or empty. Do not invent problems."""

SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["scam", "suspicious", "safe"]},
        "confidence": {"type": "integer", "minimum": 0, "maximum": 100},
        "headline": {"type": "string"},
        "impersonating": {"type": "string"},
        "red_flags": {"type": "array", "items": {
            "type": "object",
            "properties": {"quote": {"type": "string"}, "why": {"type": "string"}},
            "required": ["quote", "why"],
        }},
        "next_steps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["verdict", "confidence", "headline", "red_flags", "next_steps"],
}


def ask_gemini(parts):
    # reads GEMINI_API_KEY; per call so the app starts without it.
    # SDK retries 429s by default, burning free-tier quota; retry only server hiccups, once
    client = genai.Client(http_options={"retry_options": {"attempts": 1, "http_status_codes": [500, 502, 503, 504]}})
    kwargs = dict(model=MODEL, input=parts,
                  response_format={"type": "text", "mime_type": "application/json", "schema": SCHEMA})
    try:
        return client.interactions.create(**kwargs, tools=[{"type": "google_search"}])
    except Exception:  # incl. 429: search grounding has its own, smaller free-tier quota
        app.logger.exception("Gemini call with google_search failed; retrying without search")
        return client.interactions.create(**kwargs)


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


# ponytail: in-memory cache, lost on restart; repeat checks of the same input cost no quota
@lru_cache(maxsize=256)
def verdict_for(text, image_bytes, mime):
    parts = [{"type": "text", "text": PROMPT}]
    if text:
        parts.append({"type": "text", "text": "Message to analyze:\n" + text})
    if image_bytes:
        parts.append({"type": "image", "data": base64.b64encode(image_bytes).decode(), "mime_type": mime or "image/png"})
    return json.loads(ask_gemini(parts).output_text)


@app.post("/api/analyze")
def analyze():
    image = request.files.get("image")
    text = (request.form.get("text") or "").strip()
    if not image and not text:
        return jsonify(error="Provide an image and/or text."), 400
    try:
        return jsonify(verdict_for(text, image.read() if image else b"", image.mimetype if image else ""))
    except Exception as e:
        if getattr(e, "status_code", None) == 429:
            return jsonify(error="Gemini free-tier quota used up. Wait a minute (or until tomorrow for the daily limit) and try again."), 429
        app.logger.exception("analyze failed")
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, port=5000)
