import tga


def test_load_tga():
    img = tga.CoordinateImage()
    img.load("line_1.tga")
    print(f"w = {img._w}")
    print(f"h = {img._h}")
    pixel = img.get_pixel(13, 20)
    print(type(pixel), pixel, type(pixel[0]))
