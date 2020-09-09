from functools import WRAPPER_ASSIGNMENTS, wraps


def wraps_with_namechange(function):
    assigned = (x for x in WRAPPER_ASSIGNMENTS if x != "__name__")
    return wraps(function, assigned=assigned)
