import imp


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
