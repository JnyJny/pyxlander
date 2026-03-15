"""
"""


def will_wrap(value: int, lo: int, hi: int) -> bool:
    return value < lo or value > hi


def wrap(value: int, lo: int, hi: int) -> int:
    if value > hi:
        return lo
    if value < lo:
        return hi
    return value


def constrain(value: int | float, lo: int | float, hi: int | float) -> int | float:
    return min(hi, max(lo, value))


def wrapxy(
    x: int,
    y: int,
    w: int,
    h: int,
    ox: int = 0,
    oy: int = 0,
    randomize_on_wrap: bool = False,
) -> tuple[int, int]:

    if randomize_on_wrap:
        if will_wrap(x, ox, w):
            pass
        if will_wrap(y, oy, h):
            pass

    return wrap(x, ox, w), wrap(y, oy, h)
