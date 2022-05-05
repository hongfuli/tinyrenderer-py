from line import line
from tga import CoordinateImage
from model import Model


def test_model():
    m = Model("obj/african_head.obj")
    print("====== vert ", m.n_verts(), m.vert(0))
    print("====== face ", m.n_faces(), m.face(0))

    width = height = 800
    image = CoordinateImage(width, height)
    white = (255, 255, 255)

    for face in m.faces():
        for n_edge in range(3):
            v0 = m.vert(face[n_edge])
            v1 = m.vert(face[(n_edge + 1) % 3])
            x0 = int((v0[0] + 1) * width / 2)
            y0 = int((v0[1] + 1) * height / 2)
            x1 = int((v1[0] + 1) * width / 2)
            y1 = int((v1[1] + 1) * height / 2)

            line(x0, y0, x1, y1, image, white)

    image.save("african_head")
