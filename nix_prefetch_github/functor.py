from typing import Callable, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def map_or_none(mapping: Callable[[T], U], value: Optional[T]) -> Optional[U]:
    if value is None:
        return None
    else:
        return mapping(value)
