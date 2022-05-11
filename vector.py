import typing


class Vector2:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, o: "Vector2"):
        return Vector2(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Vector2"):
        return Vector2(self.x - o.x, self.y - o.y)

    def __mul__(self, scale: typing.Union[int, float]):
        return Vector2(int(self.x * scale), int(self.y * scale))


class Vector3:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z
