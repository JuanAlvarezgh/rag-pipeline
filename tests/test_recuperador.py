from rag import almacen, recuperador
from rag.vectorizador import VectorizadorFalso

V = VectorizadorFalso()


def test_recuperar_devuelve_el_fragmento_exacto(conexion):
    id_doc = almacen.guardar_documento(conexion, "Doc", "demo")
    textos = ["alfa primero", "beta segundo", "gamma tercero"]
    almacen.guardar_fragmentos(conexion, id_doc, textos, V.vectorizar(textos))
    res = recuperador.recuperar(conexion, V, "beta segundo", k=1)
    assert len(res) == 1
    assert res[0].texto == "beta segundo"
