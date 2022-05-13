import math
import typing


class Vector2:
    def __init__(self, x, y, n_type=int) -> None:
        self.x = n_type(x)
        self.y = n_type(y)
        self.n_type = n_type

    def __add__(self, o: "Vector2"):
        return Vector2(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Vector2"):
        return Vector2(self.x - o.x, self.y - o.y)

    def __mul__(self, scale):
        return Vector2(self.x * scale, self.y * scale, self.n_type)


class Vector3:
    def __init__(self, x, y, z, n_type=int) -> None:
        self.x = n_type(x)
        self.y = n_type(y)
        self.z = n_type(z)
        self.n_type = n_type

    def __add__(self, o: "Vector3"):
        return Vector3(self.x + o.x, self.y + o.y, self.z + o.z, self.n_type)

    def __sub__(self, o: "Vector3"):
        return Vector3(self.x - o.x, self.y - o.y, self.z - o.z, self.n_type)

    def __mul__(self, scale):
        if isinstance(scale, (int, float)):
            return Vector3(self.x * scale, self.y * scale, self.z * scale, self.n_type)
        elif isinstance(scale, Vector3):
            # dot product
            return self.x * scale.x + self.y * scale.y + self.z * scale.z

    def __xor__(self, o: "Vector3"):
        # cross product
        return Vector3(
            self.y * o.z - self.z * o.y,
            self.z * o.x - self.x * o.z,
            self.x * o.y - self.y * o.x,
            self.n_type,
        )

    def norm(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self, l=1):
        n = l / self.norm()
        self.x *= n
        self.y *= n
        self.z *= n

    def tuple_data(self, n_type):
        return (n_type(self.x), n_type(self.y), n_type(self.z))
