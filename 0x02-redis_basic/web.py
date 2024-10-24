#!/usr/bin/python3
"""
web.py
"""
import requests
import redis
from functools import wraps


redisInstance = redis.Redis()


def url_count(method):
    """
    track how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    @wraps(method)
    def wrapper(url):
        """ wrapper function. """
        cache_key = "cached:" + url
        cache_val = redisInstance.get(cache_key)
        if cache_val:
            return cache_val.decode("utf-8")
        cache_track = "count:" + url
        html_content = method(url)
        redisInstance.incr(cache_track)
        redisInstance.set(cache_key, html_content, ex=1)
        redisInstance.expire(cache_key, 10)
        return html_content
    return wrapper


@url_count
def get_page(url: str) -> str:
    """
    obtain the HTML content of a particular URL and returns it.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    r = get_page("http://slowwly.robertomurray.co.uk")
