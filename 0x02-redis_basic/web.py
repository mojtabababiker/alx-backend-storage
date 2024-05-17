#!/usr/bin/env python3
"""
tracking web url request using redis
"""
import random
from time import sleep
from typing import Callable, Any
import redis
import requests
from functools import wraps


def track_url(fn: Callable) -> Callable:
    """
    decorator to keep tracking the url with redis
    """
    _redis = redis.Redis()
    @wraps(fn)
    def tracker(url: str, *args, **kwargs) -> Any:
        """
        the main url tracker function
        """
        if url:
            key = f"count:{url}"
            if not _redis.exists(key):
                _redis.setex(key, 10, 1)
            else:
                _redis.incr(key)
            return fn(url, *args, **kwargs)
    return tracker


@track_url
def get_page(url: str) -> str:
    """
    get the html content of the url and returns it
    """
    res = requests.get(url)
    res.raise_for_status
    return res.text


if __name__ == "__main__":
    """
    _redis = redis.Redis()
    _redis.flushdb()
    for i in range(15):
        url = random.choice(["https://www.google.com",
                             "https://www.youtube.com",
                             "https://www.wikipedia.org"]
                            )
        result = get_page(url)
        call_count = _redis.get(f"count:{url}") or 0
        ttl = _redis.ttl(f"count:{url}") or 0
        print(f"The {url} page was called {int(call_count)}" +
              f" and have {int(ttl)} seconds remaining")
        sleep(random.randint(1, 5))
    """
    pass
