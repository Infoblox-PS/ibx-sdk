from functools import wraps
from warnings import warn


def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        warn(f"{func.__name__} is deprecated.", DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)

    return wrapper


@deprecated
def old_function():
    pass
