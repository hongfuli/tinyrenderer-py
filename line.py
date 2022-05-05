from tga import CoordinateImage


def line_1(x0, y0, x1, y1: int, image: CoordinateImage, color):
    t = 0.0
    while t < 1:
        x = int(x0 * (1 - t) + x1 * t)
        y = int(y0 * (1 - t) + y1 * t)
        image.set(x, y, color)
        t += 0.01


def line_2(x0, y0, x1, y1: int, image: CoordinateImage, color):
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        y = int(y0 * (1 - t) + y1 * t)
        image.set(x, y, color)


def line_3(x0, y0, x1, y1: int, image: CoordinateImage, color):
    step = abs(x1 - x0) > abs(y1 - y0)
    if not step:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        y = int(y0 * (1 - t) + y1 * t)
        if step:
            image.set(x, y, color)
        else:
            image.set(y, x, color)


def line_4(x0, y0, x1, y1: int, image: CoordinateImage, color):
    step = abs(x1 - x0) > abs(y1 - y0)
    if not step:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)
    de = dy / dx
    err = 0.0
    y = y0
    y_direction = 1 if y1 > y0 else -1
    for x in range(x0, x1 + 1):
        if step:
            image.set(x, y, color)
        else:
            image.set(y, x, color)
        err += de
        if err > 0.5:
            y += y_direction
            err -= 1


def line_5(x0, y0, x1, y1: int, image: CoordinateImage, color):
    step = abs(x1 - x0) > abs(y1 - y0)
    if not step:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)
    de = dy * 2
    err = 0.0
    y = y0
    y_direction = 1 if y1 > y0 else -1
    for x in range(x0, x1 + 1):
        if step:
            image.set(x, y, color)
        else:
            image.set(y, x, color)
        err += de
        if err > dx:
            y += y_direction
            err -= 2 * dx


line = line_5
