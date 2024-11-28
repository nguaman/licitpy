from functools import wraps
from typing import Callable, Dict, Type, TypeVar

T = TypeVar("T")


def singleton(cls: Type[T]) -> Callable[..., T]:
    instances: Dict[Type[T], T] = {}

    @wraps(cls)
    def get_instance(*args: object, **kwargs: object) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
