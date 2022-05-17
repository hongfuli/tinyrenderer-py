from dataclasses import dataclass
import re
import typing

from vector import Vector3


class Model:

    _vert_flag = "v"
    _face_flag = "f"

    def __init__(self, filename: str) -> None:

        self._verts = []
        self._faces = []

        with open(filename, "r") as f:
            for l in f:
                segs = re.split(r"[ ]+", l)
                if len(segs) != 4:
                    continue
                if segs[0] == Model._vert_flag:
                    self._verts.append(tuple([float(i) for i in segs[1:]]))
                elif segs[0] == Model._face_flag:
                    self._faces.append(
                        tuple(int(seg.split("/")[0]) - 1 for seg in segs[1:])
                    )

    def n_verts(self) -> int:
        return len(self._verts)

    def n_faces(self) -> int:
        return len(self._faces)

    def vert(self, idx: int) -> typing.Tuple[int]:
        return self._verts[idx]

    def vt(self, idx: int) -> typing.Tuple[float]:
        return self._vts[idx]

    def face(self, idx: int) -> typing.Tuple[int]:
        return self._faces[idx]

    def faces(self) -> typing.Iterable[typing.Tuple[int]]:
        for f in self._faces:
            yield f


@dataclass
class FaceData:
    vert_idx: Vector3
    texture_idx: Vector3
    # normal: Vector3


class Model1:

    _vert_flag = "v"
    _texture_flag = "vt"
    _face_flag = "f"

    def __init__(self, filename: str) -> None:

        self._verts = []
        self._textures = []
        self._faces = []

        with open(filename, "r") as f:
            for l in f:
                segs = re.split(r"[ ]+", l)
                if len(segs) != 4:
                    continue
                if segs[0] == Model1._vert_flag:
                    self._verts.append(Vector3(*[float(i) for i in segs[1:]], float))
                elif segs[0] == Model1._texture_flag:
                    self._textures.append(Vector3(*[float(i) for i in segs[1:]], float))
                elif segs[0] == Model1._face_flag:
                    flat_elements = [
                        int(idx) - 1 for seg in segs[1:] for idx in seg.split("/")
                    ]

                    self._faces.append(
                        FaceData(
                            vert_idx=Vector3(*flat_elements[0::3]),
                            texture_idx=Vector3(*flat_elements[1::3]),
                        )
                    )

    def n_verts(self) -> int:
        return len(self._verts)

    def n_faces(self) -> int:
        return len(self._faces)

    def vert(self, idx: int) -> Vector3:
        return self._verts[idx]

    def texture(self, idx: int) -> Vector3:
        return self._textures[idx]

    def face(self, idx: int) -> Vector3:
        return self._faces[idx]

    def faces(self) -> typing.Iterable[FaceData]:
        for f in self._faces:
            yield f
