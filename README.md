---
title: Exam Tutor AI
emoji: 📚
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# 📚 Exam Tutor AI

> An AI-powered exam preparation assistant for high school students in **Grades 9–12**, built with Python, Flask, and Hugging Face free inference.

---

## ✨ Features

- **Grade-aware answers** — explanations calibrated for Grades 9, 10, 11, and 12
- **6 subjects** — Mathematics, Physics, Chemistry, Biology, Computer Science, English
- **Structured answers** — every response includes:
  - 📖 Step-by-step explanation
  - 🔑 Key concepts
  - 📐 Formulas & equations
  - 🌍 Real-world example
  - 🎯 Exam tips
  - ⚠️ Common mistakes
- **4 follow-up actions** per answer:
  - 🧠 Explain Simpler
  - 💡 Give Another Example
  - 📝 Generate 5 MCQs
  - 📋 Generate Short Notes
- **Dark mode** with system preference detection
- **Copy to clipboard** button on every answer
- **Mobile responsive** — works on phones, tablets, desktops
- **Loading skeletons** for smooth UX
- **Rate limiting** — server-side protection against abuse

---

## 🗂️ Project Structure

```
exam-tutor-ai/
├── app.py                  # Flask app, routes, API endpoint
├── requirements.txt        # Python dependencies
├── Dockerfile              # For HuggingFace Spaces (Docker SDK)
├── README.md               # This file
├── .env.example            # Environment variable template
├── templates/
│   └── index.html          # Single-page UI (Tailwind CSS + vanilla JS)
└── utils/
    ├── __init__.py
    ├── huggingface.py      # HF inference client (multi-provider fallback)
    ├── prompts.py          # Prompt builders for main + action requests
    ├── constants.py        # Grades, subjects, icons, action buttons
    └── rate_limiter.py     # In-memory rate limiter
```

---

## 🚀 Deploy on HuggingFace Spaces

### 1. Create a new Space

- Go to **https://huggingface.co/new-space**
- Name it anything (e.g. `exam-tutor-ai`)
- SDK: **Docker**
- Visibility: Public or Private

### 2. Upload all files

Upload every file keeping the folder structure intact:
```
app.py
requirements.txt
Dockerfile
README.md
templates/index.html
utils/__init__.py
utils/huggingface.py
utils/prompts.py
utils/constants.py
utils/rate_limiter.py
```

### 3. Add your HF token as a secret

In your Space → **Settings** → **Variables and secrets** → **New secret**:

| Name | Value |
|------|-------|
| `HF_TOKEN` | your token from huggingface.co/settings/tokens |

Get a free token at **https://huggingface.co/settings/tokens**
- Click **New token** → select **Read** role → copy it

### 4. Your Space will build and launch automatically ✅

---

## 💻 Run Locally

```bash
# 1. Clone / download the project
cd exam-tutor-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and add your HF token

# 4. Run
python app.py

# 5. Open in browser
# http://localhost:7860
```

---

## 🤖 AI Model

The app uses **Hugging Face free inference** via `router.huggingface.co`.
It automatically tries these free providers in order until one works:

| Provider | Model |
|----------|-------|
| `novita` | `meta-llama/Llama-3.2-3B-Instruct` |
| `sambanova` | `meta-llama/Llama-3.2-3B-Instruct` |
| `featherless-ai` | `HuggingFaceH4/zephyr-7b-beta` |
| `nebius` | `meta-llama/Llama-3.2-3B-Instruct` |

No credit card. No paid plan. Just a free HF account.

---

## 🔌 API Reference

### `POST /api/ask`

**Request:**
```json
{
  "grade": "Grade 10",
  "subject": "Mathematics",
  "question": "How do I solve quadratic equations?"
}
```

**Response:**
```json
{
  "answer": "<p>...</p>",
  "raw": "## 📖 Explanation\n\n..."
}
```

**For follow-up actions**, add:
```json
{
  "grade": "Grade 10",
  "subject": "Mathematics",
  "question": "How do I solve quadratic equations?",
  "action": "generate_mcqs",
  "previousAnswer": "..."
}
```

**Action types:** `explain_simpler` · `another_example` · `generate_mcqs` · `short_notes`

### `GET /api/health`

Returns current status and model name.

---

## 🔒 Security

- API token stored in environment secrets, never in code
- Input validation on all fields (grade, subject, question length)
- Rate limiting: 20 requests per IP per minute
- No data stored — all stateless

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask 3.1 |
| Frontend | HTML, Tailwind CSS (CDN), Vanilla JS |
| AI | Hugging Face Inference API (free) |
| Hosting | HuggingFace Spaces (Docker) |

---

## 📄 License

MIT — free to use, modify, and deploy.
