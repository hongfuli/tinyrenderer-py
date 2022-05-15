import imp


import pytest
from tga import CoordinateImage
from triangle import barycentric, triange_1, triange_2
from vector import Vector2

width = height = 200
image = CoordinateImage(width, height)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)


@pytest.fixture
def image():
    return CoordinateImage(width, height)


def test_triangle_1(image):
    triange_1(Vector2(10, 70), Vector2(50, 160), Vector2(70, 80), image, white)
    triange_1(Vector2(180, 50), Vector2(150, 1), Vector2(70, 180), image, red)
    triange_1(Vector2(180, 150), Vector2(120, 160), Vector2(130, 180), image, green)
    image.save("triangle_1")


def test_barycentric():
    p = Vector2(110, 290)
    p0 = Vector2(100, 300)
    p1 = Vector2(200, 20)
    p2 = Vector2(300, 500)
    u = barycentric(p, p0, p1, p2)
    print(u)


def test_triangle_2(image):
    triange_2(Vector2(10, 70), Vector2(50, 160), Vector2(70, 80), image, white)
    # triange_2(Vector2(180, 50), Vector2(150, 1), Vector2(70, 180), image, red)
    # triange_2(Vector2(180, 150), Vector2(120, 160), Vector2(130, 180), image, green)
    image.save("triangle_2")
