import typing


class Model:

    _vert_flag = "v"
    _face_flag = "f"

    def __init__(self, filename: str) -> None:

        self._verts = []
        self._faces = []

        with open(filename, "r") as f:
            for l in f:
                segs = l.split(" ")
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

    def face(self, idx: int) -> typing.Tuple[int]:
        return self._faces[idx]
