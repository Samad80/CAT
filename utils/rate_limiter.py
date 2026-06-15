# =============================================
# Exam Tutor AI — Simple Rate Limiter
# =============================================
# In-memory rate limiter. For production,
# replace with Redis using flask-limiter.

import time
from collections import defaultdict
from threading import Lock

_lock = Lock()
_requests: dict[str, list[float]] = defaultdict(list)

WINDOW_SECONDS = 60
MAX_REQUESTS = 20


def is_rate_limited(ip: str) -> bool:
    """
    Returns True if the given IP has exceeded the rate limit.
    Allows MAX_REQUESTS per WINDOW_SECONDS.
    """
    now = time.time()
    cutoff = now - WINDOW_SECONDS

    with _lock:
        # Drop old timestamps
        _requests[ip] = [t for t in _requests[ip] if t > cutoff]

        if len(_requests[ip]) >= MAX_REQUESTS:
            return True

        _requests[ip].append(now)
        return False