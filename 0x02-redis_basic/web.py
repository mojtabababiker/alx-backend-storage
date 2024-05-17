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


_redis = redis.Redis()

def track_url(fn: Callable) -> Callable:
    """
    decorator to keep tracking the url with redis
    """

    @wraps(fn)
    def tracker(url: str, *args, **kwargs) -> Any:
        """
        the main url tracker function
        """
        key = f"count:{url}"
        _redis.incr(key)
        result = _redis.get(f"cache:{url}")
        if result:
            return result.decode("utf-8")
        else:
            result = fn(url, *args, **kwargs)
            _redis.setex(key, 10, 1)
            _redis.setex(f"cache:{url}", 10, result)

        return result
    return tracker


@track_url
def get_page(url: str) -> str:
    """
    get the html content of the url and returns it
    """
    res = requests.get(url)
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
