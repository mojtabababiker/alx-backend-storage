#!/usr/bin/env python3
"""
base cach class module
"""
import redis
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4


def count_calls(f: Callable) -> Callable:
    """
    calls number decorator function
    """
    @wraps(f)
    def counter(*args, **kwargs):
        """
        set or increament the number of calls
        for the tunction f
        """
        self = args[0]
        self._redis.incr(f.__qualname__)
        return f(*args, **kwargs)
    return counter


def call_history(f: Callable) -> Callable:
    """
    calls history decorator function
    """
    @wraps(f)
    def history(*args, **kwargs):
        """
        set a list of inputs and outputs
        for the function f
        """
        self = args[0]
        qnm = f.__qualname__
        output = f(*args, **kwargs)
        self._redis.rpush(f"{qnm}:inputs", str(args[1:]))
        self._redis.rpush(f"{qnm}:outputs", str(output))
        return output
    return history


class Cache:
    """
    basic cache class using redis
    """
    def __init__(self):
        """
        initiate the Cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """
        save data into redis instance, with randomly generated
        key, and return this key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
            str, int, float, bytes]:
        """
        retrive the value from redis with the key key, and
        if fn the fn will be called on the val
        """
        val = self._redis.get(key)
        if val and fn:
            return fn(val)
        return val

    def get_str(self, key: str) -> str:
        """
        parametrize Cache.get to convert the value into str
        """
        val = self.get(key).decode('utf-8')
        return val

    def get_int(self, key: str) -> int:
        """
        parametrize Cache.get to convert the value into int
        """
        val = int(self.get(key))
        return val


def replay(fn: Callable) -> None:
    """
    function to display the history of calls of
    a particular function
    """
    _redis = redis.Redis()
    fqname = fn.__qualname__
    callsnum = _redis.get(fqname)
    inputs = _redis.lrange(f"{fqname}:inputs", 0, -1)
    outputs = _redis.lrange(f"{fqname}:outputs", 0, -1)

    print(f"{fqname} was called {callsnum.decode('utf-8')} times:")

    for _in, _out in zip(inputs, outputs):
        print(
            f"{fqname}(*{_in.decode('utf-8')}) -> {_out.decode('utf-8')}"
        )
