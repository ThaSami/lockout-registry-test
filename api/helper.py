import toolz
import yaml
import git
import os
from functools import _lru_cache_wrapper, lru_cache

from functools import lru_cache, wraps
from datetime import datetime, timedelta

import os

def check_merged(basebranch, data):
    return (
        toolz.get_in(["pull_request", "base", "ref"], data, "unknown") == basebranch
        and toolz.get_in(["action"], data, "False") == "closed"
        and toolz.get_in(["pull_request", "merged"], data, False)
    )


def read_yaml(yamldata):
    try:
        return yaml.safe_load(yamldata)
    except yaml.YAMLError as exc:
        print(exc)


def format_service_dictionary(dictionary):
    return {
        "lockall": dictionary["lockall"],
        "lockout": set(dictionary["lockout"]) - set(dictionary["whitelist"]),
        "whitelist": set(dictionary["whitelist"]),
    }

def parse_data(yamldata):
    return format_service_dictionary(read_yaml(yamldata))

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache