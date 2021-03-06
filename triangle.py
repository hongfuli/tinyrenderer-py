import typing

from tga import CoordinateImage
from vector import Vector2, Vector3


def triange_1(p0: Vector2, p1: Vector2, p2: Vector2, image: CoordinateImage, color):
    # Line sweeping
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


def triange_2(p0: Vector2, p1: Vector2, p2: Vector2, image: CoordinateImage, color):
    # get the bounding box include the triangle
    min_x = min(p0.x, p1.x, p2.x)
    max_x = max(p0.x, p1.x, p2.x)
    min_y = min(p0.y, p1.y, p2.y)
    max_y = max(p0.y, p1.y, p2.y)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if in_triangle_by_cross_pruduct(Vector2(x, y, p0.n_type), p0, p1, p2):
                image.set(x, y, color)


def triange_with_zbuffer(
    p0: Vector3,
    p1: Vector3,
    p2: Vector3,
    width,
    height: int,
    z_buffer,
    image: CoordinateImage,
    color,
):
    # get the bounding box include the triangle
    min_x = int(min(p0.x, p1.x, p2.x))
    max_x = int(max(p0.x, p1.x, p2.x))
    min_y = int(min(p0.y, p1.y, p2.y))
    max_y = int(max(p0.y, p1.y, p2.y))

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            bc_u = barycentric(
                Vector2(x, y),
                Vector2(p0.x, p0.y),
                Vector2(p1.x, p1.y),
                Vector2(p2.x, p2.y),
            )
            if bc_u.x < 0 or bc_u.y < 0 or bc_u.z < 0:
                continue
            z_value = Vector3(p0.z, p1.z, p2.z, float) * bc_u
            idx = x + y * width
            if z_buffer[idx] < z_value:
                z_buffer[idx] = z_value
                image.set(x, y, color)


def triange_with_texture(
    screen_coords,
    texture_coords,
    width,
    height: int,
    z_buffer,
    image: CoordinateImage,
    texture: CoordinateImage,
    intensity,
):
    # get the bounding box include the triangle
    p0 = screen_coords[0]
    p1 = screen_coords[1]
    p2 = screen_coords[2]
    min_x = int(min(p0.x, p1.x, p2.x))
    max_x = int(max(p0.x, p1.x, p2.x))
    min_y = int(min(p0.y, p1.y, p2.y))
    max_y = int(max(p0.y, p1.y, p2.y))

    texture_w = texture.get_width()
    texture_h = texture.get_height()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if x > width or y > height:
                continue
            bc_u = barycentric(
                Vector2(x, y),
                Vector2(p0.x, p0.y),
                Vector2(p1.x, p1.y),
                Vector2(p2.x, p2.y),
            )
            if bc_u.x < 0 or bc_u.y < 0 or bc_u.z < 0:
                continue
            z_value = Vector3(p0.z, p1.z, p2.z, float) * bc_u

            texture_x = int(
                (
                    texture_coords[0].x * bc_u.x
                    + texture_coords[1].x * bc_u.y
                    + texture_coords[2].x * bc_u.z
                )
                * texture_w
            )
            texture_y = int(
                (
                    texture_coords[0].y * bc_u.x
                    + texture_coords[1].y * bc_u.y
                    + texture_coords[2].y * bc_u.z
                )
                * texture_h
            )
            color = texture.get_pixel(texture_x, texture_y)

            idx = x + y * width
            if z_buffer[idx] < z_value:
                z_buffer[idx] = z_value
                try:
                    image.set(x, y, [int(c * intensity) for c in color])
                except:
                    print("x = ", x, "y = ", y)
                    raise


def in_triangle_by_barycentric(p, p0, p1, p2):
    u = barycentric(p, p0, p1, p2)
    return u.x >= 0 and u.y >= 0 and u.z >= 0


def in_triangle_by_cross_pruduct(p, p0, p1, p2):
    def z_direction(v1, v2, v3):
        l1 = v2 - v1
        l2 = v3 - v1
        return l1.x * l2.y - l1.y * l2.x >= 0

    d1 = z_direction(p, p0, p1)
    d2 = z_direction(p, p1, p2)
    d3 = z_direction(p, p2, p0)
    return d1 == d2 and d2 == d3


def barycentric(p, p0, p1, p2) -> Vector3:
    # AP = uAB + vAC  ==> P = (1 - u - v)A + uB + vC
    # return (1 - u - v, u, v)
    u = Vector3(p2.x - p0.x, p1.x - p0.x, p0.x - p.x, float) ^ Vector3(
        p2.y - p0.y, p1.y - p0.y, p0.y - p.y, float
    )
    if abs(u.z) < 0.01:
        return Vector3(-1, 1, 1, float)
    return Vector3(1 - ((u.x + u.y) / u.z), u.x / u.z, u.y / u.z, float)


triangle = triange_2
