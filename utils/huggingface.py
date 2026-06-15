# =============================================
# Exam Tutor AI — Hugging Face Inference Client
# =============================================
# Uses huggingface_hub.InferenceClient which
# routes via router.huggingface.co — works on
# HF Spaces without any DNS issues.

import os
from huggingface_hub import InferenceClient


def call_huggingface(prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
    # On HF Spaces the token is auto-injected as HF_TOKEN
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN", "")
    if not token:
        raise ValueError(
            "API token not set. In your Space go to: "
            "Settings → Variables and secrets → New secret → "
            "Name: HF_TOKEN, Value: your token from huggingface.co/settings/tokens"
        )

    model = os.environ.get("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")

    client = InferenceClient(model=model, token=token)

    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        err = str(e)
        if "401" in err or "Unauthorized" in err:
            raise ValueError(
                "Invalid token. Check HF_TOKEN in your Space secrets — "
                "get one at huggingface.co/settings/tokens"
            )
        if "403" in err or "license" in err.lower() or "access" in err.lower():
            raise ValueError(
                f'Access denied to "{model}". '
                f"Accept its license at huggingface.co/{model} "
                "or change HUGGINGFACE_MODEL in your Space settings."
            )
        if "404" in err:
            raise ValueError(f'Model "{model}" not found. Check HUGGINGFACE_MODEL in your Space settings.')
        if "429" in err:
            raise RuntimeError("Rate limit reached. Wait a moment and try again.")
        if "503" in err or "loading" in err.lower():
            raise RuntimeError("Model is loading. Wait ~30 seconds and try again.")
        raise RuntimeError(f"Inference error: {err}")