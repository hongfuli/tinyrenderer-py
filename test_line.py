import pytest

import tga
import line


@pytest.fixture
def image():
    return tga.CoordinateImage(100, 100)


def test_line_1(image):
    red = (255, 0, 0)
    line.line_1(13, 20, 80, 40, image, red)
    image.save("line_1")


def test_line_2(image):
    red = (255, 0, 0)
    white = (255, 255, 255)
    line.line_2(13, 20, 80, 40, image, white)
    line.line_2(20, 13, 40, 80, image, red)
    line.line_2(80, 40, 13, 20, image, red)
    image.save("line_2")


def test_line_3(image):
    red = (255, 0, 0)
    white = (255, 255, 255)
    line.line_3(13, 20, 80, 40, image, white)
    line.line_3(20, 13, 40, 80, image, red)
    line.line_3(80, 40, 13, 20, image, red)
    image.save("line_3")


def test_line_4(image):
    red = (255, 0, 0)
    white = (255, 255, 255)
    line.line_4(13, 20, 80, 40, image, white)
    line.line_4(20, 13, 40, 80, image, red)
    line.line_4(80, 40, 13, 20, image, red)
    image.save("line_4")


def test_line_5(image):
    red = (255, 0, 0)
    white = (255, 255, 255)
    line.line_5(13, 20, 80, 40, image, white)
    line.line_5(20, 13, 40, 80, image, red)
    line.line_5(80, 40, 13, 20, image, red)
    image.save("line_5")


@pytest.fixture
def image_1():
    return tga.CoordinateImage(800, 800)


def test_line_5_1(image_1):
    white = (255, 255, 255)
    line.line_5(400, 799, 400, 800, image_1, white)
    image_1.save("line_5")
