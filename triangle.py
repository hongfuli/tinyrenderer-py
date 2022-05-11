import typing

from tga import CoordinateImage
from vector import Vector2


def triange_1(p0: Vector2, p1: Vector2, p2: Vector2, image: CoordinateImage, color):
    # p0, p1, p2 are point with (x, y)

    # degenerate
    if p0.y == p1.y == p2.y:
        return

    # sort points by their y value
    p0, p1, p2 = sorted([p0, p1, p2], key=lambda p: p.y)

    total_h = p2.y - p0.y
    for i in range(total_h):
        is_top_half = i > (p1.y - p0.y) or (p0.y == p1.y)
        segment_h = p2.y - p1.y if is_top_half else p1.y - p0.y
        alpha = i / total_h
        beta = ((i - (p1.y - p0.y)) if is_top_half else i) / segment_h
        A = p0 + (p2 - p0) * alpha
        B = p1 + (p2 - p1) * beta if is_top_half else p0 + (p1 - p0) * beta
        if A.x > B.x:
            A, B = B, A
        for x in range(A.x, B.x + 1):
            image.set(x, p0.y + i, color)
