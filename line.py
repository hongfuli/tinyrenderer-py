from tga import CoordinateImage


def line_1(x0, y0, x1, y1: int, image: CoordinateImage, color):
    t = 0.0
    while t < 1:
        x = int(x0 * (1 - t) + x1 * t)
        y = int(y0 * (1 - t) + y1 * t)
        image.set(x, y, color)
        t += 0.1
