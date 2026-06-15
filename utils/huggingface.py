# =============================================
# Exam Tutor AI — Hugging Face API Client
# =============================================
# Uses router.huggingface.co with multiple
# free inference providers as fallbacks.

import os
import requests


# Provider + model combinations that are free and require no license.
# router.huggingface.co routes to these automatically.
FREE_PROVIDERS = [
    # provider,         model
    ("novita",          "meta-llama/Llama-3.2-3B-Instruct"),
    ("sambanova",       "meta-llama/Llama-3.2-3B-Instruct"),
    ("featherless-ai",  "HuggingFaceH4/zephyr-7b-beta"),
    ("nebius",          "meta-llama/Llama-3.2-3B-Instruct"),
]


def call_huggingface(prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN", "")
    if not token:
        raise ValueError(
            "Token not set. In your Space: Settings → Variables and secrets → "
            "New secret → Name: HF_TOKEN, Value: your token from huggingface.co/settings/tokens"
        )

    # Allow override via env var (format: "provider/model")
    override = os.environ.get("HUGGINGFACE_MODEL", "")
    if "/" in override and override.count("/") >= 2:
        # e.g. "novita/meta-llama/Llama-3.2-3B-Instruct"
        parts = override.split("/", 1)
        providers_to_try = [(parts[0], parts[1])]
    else:
        providers_to_try = FREE_PROVIDERS

    last_error = ""
    for provider, model in providers_to_try:
        url = f"https://router.huggingface.co/{provider}/v1/chat/completions"
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
            last_error = f"[{provider}] Connection failed: {e}"
            continue
        except requests.exceptions.Timeout:
            last_error = f"[{provider}] Timed out"
            continue

        if resp.status_code == 401:
            raise ValueError(
                "Invalid token. Check HF_TOKEN in your Space secrets — "
                "get a fresh one at huggingface.co/settings/tokens"
            )

        if resp.ok:
            try:
                return resp.json()["choices"][0]["message"]["content"].strip()
            except (KeyError, IndexError) as e:
                last_error = f"[{provider}] Unexpected response format: {e}"
                continue

        last_error = f"[{provider}] HTTP {resp.status_code}: {resp.text[:150]}"
        # Keep trying next provider

    raise RuntimeError(
        f"All inference providers failed. Last error: {last_error}\n"
        "Check that your HF_TOKEN is valid and has Read permissions."
    )