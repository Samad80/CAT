# =============================================
# Exam Tutor AI — Hugging Face API Client
# =============================================

import os
import requests


def call_huggingface(prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
    token = os.environ.get("HUGGINGFACE_API_TOKEN", "")
    if not token:
        raise ValueError(
            "HUGGINGFACE_API_TOKEN secret is not set. "
            "In your Space: Settings → Variables and secrets → New secret → "
            "Name: HUGGINGFACE_API_TOKEN, Value: your token from huggingface.co/settings/tokens"
        )

    model = os.environ.get("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")
    url   = f"https://api-inference.huggingface.co/models/{model}/v1/chat/completions"

    try:
        response = requests.post(
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
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"Could not connect to Hugging Face API: {e}")

    if response.status_code == 401:
        raise ValueError("Invalid token. Check your HUGGINGFACE_API_TOKEN secret in Space settings.")
    if response.status_code == 403:
        raise ValueError(
            f'Access denied to "{model}". '
            f"Accept its license at huggingface.co/{model} "
            "or set HUGGINGFACE_MODEL to a different model in Space settings."
        )
    if response.status_code == 404:
        raise ValueError(f'Model "{model}" not found. Check your HUGGINGFACE_MODEL setting.')
    if response.status_code == 503:
        raise RuntimeError("Model is loading. Wait ~30 seconds and try again.")
    if response.status_code == 429:
        raise RuntimeError("Rate limit reached. Wait a moment and try again.")
    if not response.ok:
        raise RuntimeError(f"API error ({response.status_code}): {response.text[:200]}")

    content = response.json()["choices"][0]["message"]["content"]
    return content.strip()