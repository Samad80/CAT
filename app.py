# =============================================
# Exam Tutor AI — Flask Application
# =============================================

import os
import markdown as md
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from utils.constants import (
    GRADES, SUBJECTS, SUBJECT_ICONS, SUBJECT_COLORS,
    ACTION_BUTTONS, VALID_ACTIONS, EXAMPLE_QUESTIONS,
)
from utils.prompts import build_main_prompt, build_action_prompt
from utils.huggingface import call_huggingface
from utils.rate_limiter import is_rate_limited

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-in-production")


# ── Template globals ──────────────────────────────────────────────────────────

@app.context_processor
def inject_globals():
    return {
        "grades":            GRADES,
        "subjects":          SUBJECTS,
        "subject_icons":     SUBJECT_ICONS,
        "subject_colors":    SUBJECT_COLORS,
        "action_buttons":    ACTION_BUTTONS,
        "example_questions": EXAMPLE_QUESTIONS,
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask():
    ip = (
        request.headers.get("X-Forwarded-For", request.remote_addr or "127.0.0.1")
        .split(",")[0].strip()
    )
    if is_rate_limited(ip):
        return jsonify({"error": "Too many requests. Please wait a moment."}), 429

    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Invalid request body."}), 400

    grade           = body.get("grade", "").strip()
    subject         = body.get("subject", "").strip()
    question        = body.get("question", "").strip()
    action          = body.get("action", "").strip()
    previous_answer = body.get("previousAnswer", "").strip()

    if grade not in GRADES:
        return jsonify({"error": "Invalid grade selected."}), 400
    if subject not in SUBJECTS:
        return jsonify({"error": "Invalid subject selected."}), 400
    if not question:
        return jsonify({"error": "Question is required."}), 400
    if len(question) < 5:
        return jsonify({"error": "Question too short (min 5 characters)."}), 400
    if len(question) > 2000:
        return jsonify({"error": "Question too long (max 2000 characters)."}), 400
    if action and action not in VALID_ACTIONS:
        return jsonify({"error": "Invalid action type."}), 400

    if action and previous_answer:
        prompt = build_action_prompt(action, grade, subject, previous_answer)
    else:
        prompt = build_main_prompt(grade, subject, question)

    try:
        raw  = call_huggingface(prompt)
        html = md.markdown(raw, extensions=["extra", "nl2br", "sane_lists"])
        return jsonify({"answer": html, "raw": raw}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "model": os.environ.get("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta"),
    })


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # HuggingFace Spaces requires port 7860
    port = int(os.environ.get("PORT", 7860))
    app.run(debug=False, host="0.0.0.0", port=port)