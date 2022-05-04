from model import Model


def test_model():
    m = Model("obj/african_head.obj")
    print("====== vert ", m.n_verts(), m.vert(0))
    print("====== face ", m.n_faces(), m.face(0))
