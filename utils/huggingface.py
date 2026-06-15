# =============================================
# Exam Tutor AI — Hugging Face API Client
# =============================================

import os
import requests


def call_huggingface(prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN", "")
    if not token:
        raise ValueError(
            "Token not set. In your Space: Settings → Variables and secrets → "
            "New secret → Name: HF_TOKEN, Value: your token from huggingface.co/settings/tokens"
        )

    model = os.environ.get("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")

    # router.huggingface.co resolves correctly on HF Spaces
    url = f"https://router.huggingface.co/hf-inference/models/{model}/v1/chat/completions"

    try:
        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            },
            timeout=60,
        )
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"Connection failed: {e}")
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Please try again.")

    if resp.status_code == 401:
        raise ValueError(
            "Invalid token. Check HF_TOKEN in your Space secrets — "
            "get one at huggingface.co/settings/tokens"
        )
    if resp.status_code == 403:
        raise ValueError(
            f'Access denied to "{model}". '
            f"Accept its license at huggingface.co/{model} "
            "or change HUGGINGFACE_MODEL to a different model."
        )
    if resp.status_code == 404:
        raise ValueError(f'Model "{model}" not found. Check HUGGINGFACE_MODEL in your Space settings.')
    if resp.status_code == 429:
        raise RuntimeError("Rate limit reached. Wait a moment and try again.")
    if resp.status_code == 503:
        raise RuntimeError("Model is loading. Wait ~30 seconds and try again.")
    if not resp.ok:
        raise RuntimeError(f"API error ({resp.status_code}): {resp.text[:200]}")

    return resp.json()["choices"][0]["message"]["content"].strip()