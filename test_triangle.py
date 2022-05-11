import imp


import pytest
from tga import CoordinateImage
from triangle import triange_1
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
