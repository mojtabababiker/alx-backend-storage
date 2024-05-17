#!/usr/bin/env python3
"""
base cach class module
"""
from typing import Union, Optional, Callable
import redis
from functools import wraps
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """
    calls number decorator function
    """
    @wraps(method)
    def counter(self, *args, **kwargs) -> Callable:
        """
        set or increment the number of calls
        for the function f
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return counter


def call_history(method: Callable) -> Callable:
    """
    calls history decorator function
    """
    @wraps(method)
    def history(self, *args, **kwargs) -> Callable:
        """
        set a list of inputs and outputs
        for the function f
        """
        qnm = method.__qualname__
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{qnm}:inputs", str(args))
        self._redis.rpush(f"{qnm}:outputs", str(output))
        return output
    return history


class Cache:
    """
    basic cache class using redis
    """
    def __init__(self) -> None:
        """
        initiate the Cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        save data into redis instance, with randomly generated
        key, and return this key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[
                str, int, float, bytes]:
        """
        retrieve the value from redis with the key key, and
        if fn the fn will be called on the val
        """
        val = self._redis.get(key)
        if val is not None:
            if fn:
                return fn(val)
            return val
        return ""

    def get_str(self, key: str) -> str:
        """
        parametrize Cache.get to convert the value into str
        """
        val = self.get(key)
        return val.decode('utf-8') if isinstance(val, bytes) else ""

    def get_int(self, key: str) -> int:
        """
        parametrize Cache.get to convert the value into int
        """
        val = self.get(key)
        return int(val) if isinstance(val, (str, bytes)) else 0


def replay(fn: Callable) -> None:
    """
    function to display the history of calls of
    a particular function
    """
    _redis = redis.Redis()
    fqname = fn.__qualname__
    callsnum = _redis.get(fqname) or 0
    inputs = _redis.lrange(f"{fqname}:inputs", 0, -1)
    outputs = _redis.lrange(f"{fqname}:outputs", 0, -1)

    print(f"{fqname} was called {int(callsnum)} times:")

    for _in, _out in zip(inputs, outputs):
        print(f"{fqname}(*{_in.decode('utf-8')}) -> {_out.decode('utf-8')}")
