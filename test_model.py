from collections import defaultdict
import numpy as np
import typing
from line import line
from tga import CoordinateImage
import triangle
from model import Model, Model1
from vector import Vector2, Vector3


def test_model_wire_mesh():
    m = Model("obj/african_head.obj")

    width = height = 800
    image = CoordinateImage(width, height)
    white = (255, 255, 255)

    for face in m.faces():
        for n_edge in range(3):
            v0 = m.vert(face[n_edge])
            v1 = m.vert(face[(n_edge + 1) % 3])
            x0 = int((v0[0] + 1) * width / 2)
            y0 = int((v0[1] + 1) * height / 2)
            x1 = int((v1[0] + 1) * width / 2)
            y1 = int((v1[1] + 1) * height / 2)

            line(x0, y0, x1, y1, image, white)

    image.save("african_head_wire")


def test_model_triangle():
    m = Model("obj/african_head.obj")

    width = height = 800
    image = CoordinateImage(width, height)
    white = (255, 255, 255)

    light = Vector3(0, 0, -1, float)

    for face in m.faces():
        screen_coords: typing.List[Vector2] = []
        world_coords: typing.List[Vector3] = []
        for n_edge in range(3):
            v0 = Vector3(*m.vert(face[n_edge]), float)
            screen_coords.append(
                Vector2((v0.x + 1) * width / 2, (v0.y + 1) * height / 2)
            )
            world_coords.append(v0)
        n = (world_coords[2] - world_coords[0]) ^ (world_coords[1] - world_coords[0])
        n.normalize()
        intensity = light * n
        if intensity > 0:
            triangle.triangle(
                screen_coords[0],
                screen_coords[1],
                screen_coords[2],
                image,
                (int(255 * intensity), int(255 * intensity), int(255 * intensity)),
            )

    image.save("african_head_triangle")


def test_model_triangle_with_zbuffer():
    m = Model("obj/african_head.obj")

    width = height = 800
    image = CoordinateImage(width, height)
    white = (255, 255, 255)

    light = Vector3(0, 0, -1, float)

    z_buffer = defaultdict(lambda: -100)
    for face in m.faces():
        screen_coords: typing.List[Vector3] = []
        world_coords: typing.List[Vector3] = []
        for n_edge in range(3):
            v0 = Vector3(*m.vert(face[n_edge]), float)
            screen_coords.append(
                Vector3(
                    (v0.x + 1) * width / 2 + 0.5,
                    (v0.y + 1) * height / 2 + 0.5,
                    v0.z,
                    float,
                )
            )
            world_coords.append(v0)
        n = (world_coords[2] - world_coords[0]) ^ (world_coords[1] - world_coords[0])
        n.normalize()
        intensity = light * n
        if intensity > 0:
            triangle.triange_with_zbuffer(
                screen_coords[0],
                screen_coords[1],
                screen_coords[2],
                width,
                height,
                z_buffer,
                image,
                (int(255 * intensity), int(255 * intensity), int(255 * intensity)),
            )

    image.save("african_head_triangle_with_zbuffer")


def test_model_triangle_with_texture():
    m = Model1("obj/african_head.obj")
    texture = CoordinateImage()
    texture.load("obj/african_head_diffuse.tga")

    width = height = 800
    image = CoordinateImage(width, height)

    light = Vector3(0, 0, -1, float)
    z_buffer = defaultdict(lambda: -100)
    for face in m.faces():
        screen_coords: typing.List[Vector3] = []
        world_coords: typing.List[Vector3] = []
        texture_coords: typing.List[Vector3] = []  # texture coords
        for idx in range(3):
            v0 = m.vert(face.vert_idx[idx])
            screen_coords.append(
                Vector3(
                    (v0.x + 1) * width / 2 + 0.5,
                    (v0.y + 1) * height / 2 + 0.5,
                    v0.z,
                    float,
                )
            )
            world_coords.append(v0)
            texture_coords.append(m.texture(face.texture_idx[idx]))

        n = (world_coords[2] - world_coords[0]) ^ (world_coords[1] - world_coords[0])
        n.normalize()
        intensity = light * n
        if intensity > 0:
            triangle.triange_with_texture(
                screen_coords,
                texture_coords,
                width,
                height,
                z_buffer,
                image,
                texture,
                intensity,
            )

    image.save("african_head_triangle_with_texture")


def test_model_triangle_with_perspective():
    m = Model1("obj/african_head.obj")
    texture = CoordinateImage()
    texture.load("obj/african_head_diffuse.tga")

    width = height = 800
    depth = 255
    image = CoordinateImage(width, height)

    light = Vector3(0, 0, -1, float)
    camera = Vector3(0, 0, 3, float)
    z_buffer = defaultdict(lambda: -1000)
    projection = np.identity(4)
    projection[3][2] = -1 / camera.z
    viewport = np.identity(4)
    viewport[0][3] = 400.0
    viewport[1][3] = 400.0
    viewport[2][3] = depth / 2.0
    viewport[0][0] = width / 2.0
    viewport[1][1] = height / 2.0
    viewport[2][2] = depth / 2.0
    transfer_matrix = viewport.dot(projection)

    for face in m.faces():
        screen_coords: typing.List[Vector3] = []
        world_coords: typing.List[Vector3] = []
        texture_coords: typing.List[Vector3] = []  # texture coords
        for idx in range(3):
            v0 = m.vert(face.vert_idx[idx])
            v0_t = transfer_matrix.dot(np.array([[v0.x], [v0.y], [v0.z], [1.0]]))
            screen_coords.append(
                Vector3(
                    v0_t[0][0] / v0_t[3][0],
                    v0_t[1][0] / v0_t[3][0],
                    v0_t[2][0] / v0_t[3][0],
                    float,
                )
            )
            world_coords.append(v0)
            texture_coords.append(m.texture(face.texture_idx[idx]))

        n = (world_coords[2] - world_coords[0]) ^ (world_coords[1] - world_coords[0])
        n.normalize()
        intensity = light * n
        if intensity > 0:
            triangle.triange_with_texture(
                screen_coords,
                texture_coords,
                width,
                height,
                z_buffer,
                image,
                texture,
                intensity,
            )

    image.save("african_head_triangle_with_perspective")
