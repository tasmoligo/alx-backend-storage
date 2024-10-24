#!/usr/bin/env python3
"""
exercise.py
"""
import redis
from typing import Union, Optional, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    returns a Callable
    """
    data = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wraper function. """
        self._redis.incr(data)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    stores the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function. """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """
    displays the history of calls of a particular function.
    """
    redisInstance = redis.Redis()
    funct = fn.__qualname__
    data = redisInstance.get(funct)
    try:
        data = int(data.decode("utf-8"))
    except Exception:
        data = 0
    print("{} was called {} times:".format(funct, data))
    input = redisInstance.lrange("{}:inputs".format(funct), 0, -1)
    output = redisInstance.lrange("{}:inputs".format(funct), 0, -1)
    for inp, out in zip(input, output):
        try:
            input = inp.decode("utf-8")
        except Exception:
            input = ""
        try:
            outut = out.decode("utf-8")
        except Exception:
            output = ""
        print("{}(*({})) -> {}".format(funct, input, output))


class Cache:
    """
    Create a Cache class
    """
    def __init__(self):
        """
        store an instance of the Redis client as a private variable named
        _redis and flush the instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key, store the input data in Redis using the random
        key and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """
        convert the data back to the desired format
        """
        data = self._redis.get(key)
        if fn:
            data = fn(key)
        return data

    def get_str(self, key: str) -> str:
        """
        automatically parametrize Cache.get with the correct
        conversion function.
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        automatically parametrize Cache.get with the correct
        conversion function
        """
        data = self._redis.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0
        return data
