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
                result = fn(url, *args, **kwargs)
                _redis.setex(key, 10, 0)
                _redis.setex(url, 10, result)
            else:
                result = _redis.get(url) or ""
                result = result.decode("utf-8")

            _redis.incr(key)
            return result
    return tracker


@track_url
def get_page(url: str) -> str:
    """
    get the html content of the url and returns it
    """
    res = requests.get(url)
    res.raise_for_status
    return res.text


"""
if __name__ == "__main__":
    url = "http://google.com"
    _redis = redis.Redis()
    _redis.flushdb()
    for _ in range(7):
        result = get_page(url)[: 30]
        cc = int(_redis.get(f"count:{url}"))
        ttl = int(_redis.ttl(url))
        print(f"{url} called {cc} times, and have {ttl} seconds left")
        print(f"the result is:\n\t{result}")
        print("="*20)

        sleep(random.randint(1, 5))
"""
